This article focuses on single-threaded optimizations for matrix multiplication, with parallelization being a topic for future exploration.

### Setup

The setup for this exploration includes a Ryzen 5600H processor, which has 6 cores and 12 threads. Each core is equipped with 32 KiB of L1d and L1i cache, as well as 512 KiB of L2 cache. All cores share a 16 MiB L3 cache. The compiler used is clang 18.1.3 on Ubuntu 24.04.

### Matrix Multiplication Review

Given two matrices, A (with dimensions n rows and k columns) and B (with dimensions k rows and m columns), their product, AB, is a matrix C with dimensions n rows and m columns. The element C[r][c] is the dot product of row r of A and column c of B.

In summation notation:
C[r][c] = Σ(i=0 to k-1) A[r][i] * B[i][c]

This mathematical definition will serve as the starting point for our implementation.

### Naive Implementation

The naive implementation directly translates the mathematical definition into C code. For simplicity, we'll assume the matrices are square and their dimensions are powers of 2.

The `restrict` keyword is used to inform the compiler that no other pointer will access the object, which can lead to more optimized code.

### Storing Matrices in Memory

Column-major order is a method of storing matrices in memory where columns are laid out sequentially. This is the approach used by Fortran and many BLAS libraries, including AMD’s BLI. In C/C++, the default is row-major order.

### Measuring Performance

We'll measure the time it takes to multiply two 4096x4096 matrices of doubles. Large matrices are chosen because some optimizations are more evident when the matrices do not fit entirely in the cache. With N=4096, the total size of the three matrices is 384 MiB, which is much larger than the 16 MiB L3 cache.

When compiling the code, we'll enable all relevant optimization flags from the start to maintain transparency. The following flags will be used unless otherwise specified:
```
clang main.c matmul.c -std=gnu11 -O3 -DNDEBUG -march=native -mfma -ffast-math -mavx2 -lrt -lblis -o matmul
```

### Baselines

With the code compiled, we can establish our baselines. The naive implementation multiplies two 4096x4096 matrices in approximately 480 seconds. In contrast, the highly optimized `bli_dgemm` completes the same operation in about 2.6 seconds, which is nearly 200 times faster.

### Searching for Bottlenecks

Running the naive implementation through `perf` to collect performance counters (using N=1024 to speed up profiling) reveals a surprisingly high cache miss rate. Visualizing memory access patterns shows that while we access sequential elements in a row in the logical representation, these elements are N elements apart in memory due to the column-major order.

This leads to a significant issue for large matrices. Each access requires reading a new cache line from main memory. By the time the loop returns to the first element, the original cache line has likely been evicted, forcing it to be refetched.

### Loop Reordering

To address this, we can reorder the loops. Instead of the r, c, k order, we can iterate in a way that is more cache-friendly. The orders c, k, r and k, c, r are compelling alternatives.

Measurements show that the c, k, r order performs significantly better, reducing the execution time to about 20.8 seconds. This simple change improves performance by approximately 20 times. Re-running `perf stat` shows a reduction in L3 cache misses by about 50 times.

### Inspecting Assembly

Reordering the loops not only improves the access pattern but also allows the compiler to vectorize some operations.

#### Non-vectorized

With vectorization disabled, the assembly for the inner loop shows that `clang` applies a loop unrolling optimization with a factor of 2. This means that in each inner loop iteration, it calculates both C[r][c] and C[r+1][c]. This amortizes the cost of loop overhead.

#### Vectorized

Modern CPUs support SIMD (single instruction, multiple data) instructions, which allow a single instruction to operate on multiple registers in parallel. Using compiler flags like `-mavx2` enables the generation of vectorized code.

With AVX2, each register (ymm) can hold 256 bits, or four doubles. This means that instructions like `vmulpd`, `vaddpd`, and `vmovupd` can process four multiplications, additions, and stores in parallel. The compiler also unrolls the loop with a factor of 4, resulting in 16 writes to C in each inner loop execution.

This should ideally lead to a 4x speedup, but in practice, the improvement is a more modest 1.5x.

### Cache Utilization

The next optimization is a powerful but unintuitive one. In the current implementation, the entire matrix A is scanned N times. Ideally, each element would be loaded once, used in all necessary computations, and then evicted.

To achieve this, we can restructure the product of two large matrices into products of smaller matrices. This technique, known as tiling, allows us to tune the size of the smaller matrices so that they fit nicely in the cache.

### Tiling

With tiling, we can reduce the number of cache misses by a factor proportional to the tile size. The implementation becomes more complex with the addition of tiling loops, but the amount of work remains the same; it's just reordered to better utilize the cache.

Experimenting with different tile sizes reveals that 128 is optimal, reducing the execution time to 6.6 seconds. This is a 3x improvement, bringing us to about 30% of `bli_dgemm`'s performance.

### Tile Size Analysis

Interestingly, the number of L3 and L2 cache misses for the tiled implementation is significantly worse than for the previous version. However, the number of L3 reads is lower by about 10 billion. The improved performance is likely due to the CPU's ability to hide read latencies by overlapping reads and computations, thanks to aggressive unrolling in the tiling block.

### Cache Hardware

Caches are not fully associative. They are partitioned into sets of k cache lines. An address is mapped to a specific set, and the cache line can only be stored in that set.

This can lead to cache set conflicts. If multiple addresses map to the same set, they will compete for the limited number of cache lines in that set. This can cause conflict misses, where a line is evicted because its set is full.

### Packing

To avoid these conflicts, we can copy tiles into contiguous arrays before performing the tile-tile matrix multiplication. This ensures that the tile is uniformly distributed across different cache sets. While this introduces the overhead of copying, the improved cache hit rate can compensate for it.

With packing and the inner loops extracted into a separate function (which helps the compiler with register allocation), the execution time is reduced to about 4.4 seconds. This is about 60% of `bli_dgemm`'s performance and over 100 times faster than the naive implementation.

### Next Steps

There are many more optimizations that could be explored, such as adding more levels of tiling for L2 and L1 caches, using compiler intrinsics for SIMD instructions, and experimenting with memory prefetching. However, these will be left for a potential follow-up article.

For those interested in learning more, the following resources are recommended:
- MIT’s 6.172 on OCW
- Simon’s matrix multiplication article
- The OpenBLAS repository on GitHub
