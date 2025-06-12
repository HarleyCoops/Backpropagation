"""
Backpropagation Through Time (BPTT) - NumPy Implementation
----------------------------------------------------------
A minimal, transparent implementation of BPTT for a simple RNN,
faithfully following Werbos's original equations and pseudocode.

References:
- Werbos, P.J. "Backpropagation Through Time: What It Does and How to Do It" (BP.tex)
- BP_review.md (project summary)

This code is intended for educational purposes as part of the Backpropagation Museum Project.
"""

import numpy as np

def sigmoid(z):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    """Derivative of the sigmoid function."""
    s = sigmoid(z)
    return s * (1 - s)

class SimpleRNNBPTT:
    """
    Simple RNN with Backpropagation Through Time (BPTT) using NumPy.
    - One hidden layer, fully connected, with recurrent connections.
    - Batch learning (weights updated after full sequence).
    - Follows the notation and structure of Werbos's original paper.
    """

    def __init__(self, input_size, hidden_size, output_size, seq_length, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.seq_length = seq_length
        self.learning_rate = learning_rate

        # Weight matrices
        self.W_in = np.random.randn(hidden_size, input_size) * 0.1  # Input to hidden
        self.W_rec = np.random.randn(hidden_size, hidden_size) * 0.1  # Hidden to hidden (recurrent)
        self.W_out = np.random.randn(output_size, hidden_size) * 0.1  # Hidden to output

        # Biases
        self.b_h = np.zeros((hidden_size, 1))
        self.b_y = np.zeros((output_size, 1))

    def forward(self, X_seq):
        """
        Forward pass through the sequence.
        X_seq: shape (seq_length, input_size)
        Returns:
            - h_list: list of hidden states (seq_length+1, hidden_size, 1)
            - y_list: list of outputs (seq_length, output_size, 1)
            - z_list: list of pre-activations for hidden (seq_length, hidden_size, 1)
        """
        h_prev = np.zeros((self.hidden_size, 1))
        h_list = [h_prev]
        y_list = []
        z_list = []

        for t in range(self.seq_length):
            x_t = X_seq[t].reshape(-1, 1)
            z_t = np.dot(self.W_in, x_t) + np.dot(self.W_rec, h_prev) + self.b_h
            h_t = sigmoid(z_t)
            y_t = np.dot(self.W_out, h_t) + self.b_y

            h_list.append(h_t)
            y_list.append(y_t)
            z_list.append(z_t)
            h_prev = h_t

        return h_list, y_list, z_list

    def compute_loss(self, Y_pred, Y_true):
        """
        Mean squared error loss over the sequence.
        Y_pred, Y_true: lists of (output_size, 1) arrays
        """
        loss = 0.0
        for y_pred, y_true in zip(Y_pred, Y_true):
            loss += 0.5 * np.sum((y_pred - y_true.reshape(-1, 1)) ** 2)
        return loss / len(Y_pred)

    def backward(self, X_seq, Y_true, h_list, y_list, z_list):
        """
        Backward pass (BPTT) to compute gradients.
        Returns gradients for all weights and biases.
        """
        # Initialize gradients
        dW_in = np.zeros_like(self.W_in)
        dW_rec = np.zeros_like(self.W_rec)
        dW_out = np.zeros_like(self.W_out)
        db_h = np.zeros_like(self.b_h)
        db_y = np.zeros_like(self.b_y)

        dh_next = np.zeros((self.hidden_size, 1))

        for t in reversed(range(self.seq_length)):
            y_pred = y_list[t]
            y_true = Y_true[t].reshape(-1, 1)
            h_t = h_list[t+1]
            h_prev = h_list[t]
            z_t = z_list[t]
            x_t = X_seq[t].reshape(-1, 1)

            # Output layer gradients
            dy = y_pred - y_true  # dE/dy
            dW_out += np.dot(dy, h_t.T)
            db_y += dy

            # Hidden layer gradients (BPTT)
            dh = np.dot(self.W_out.T, dy) + dh_next  # dE/dh_t
            dz = dh * sigmoid_derivative(z_t)        # dE/dz_t

            dW_in += np.dot(dz, x_t.T)
            dW_rec += np.dot(dz, h_prev.T)
            db_h += dz

            dh_next = np.dot(self.W_rec.T, dz)  # Propagate to previous time step

        # Average gradients over sequence
        for grad in [dW_in, dW_rec, dW_out, db_h, db_y]:
            grad /= self.seq_length

        return dW_in, dW_rec, dW_out, db_h, db_y

    def update_weights(self, dW_in, dW_rec, dW_out, db_h, db_y):
        """Update weights and biases using computed gradients."""
        self.W_in -= self.learning_rate * dW_in
        self.W_rec -= self.learning_rate * dW_rec
        self.W_out -= self.learning_rate * dW_out
        self.b_h -= self.learning_rate * db_h
        self.b_y -= self.learning_rate * db_y

    def train(self, X_seq, Y_seq, epochs=1000, verbose=100):
        """
        Train the RNN using BPTT.
        X_seq: shape (seq_length, input_size)
        Y_seq: shape (seq_length, output_size)
        """
        for epoch in range(1, epochs + 1):
            h_list, y_list, z_list = self.forward(X_seq)
            loss = self.compute_loss(y_list, Y_seq)
            dW_in, dW_rec, dW_out, db_h, db_y = self.backward(X_seq, Y_seq, h_list, y_list, z_list)
            self.update_weights(dW_in, dW_rec, dW_out, db_h, db_y)

            if epoch % verbose == 0 or epoch == 1:
                print(f"Epoch {epoch}: Loss = {loss:.6f}")

# Example usage (for demonstration/testing)
if __name__ == "__main__":
    np.random.seed(42)
    seq_length = 5
    input_size = 2
    hidden_size = 4
    output_size = 1

    # Generate a toy sequence problem (e.g., sum of inputs)
    X_seq = np.random.randn(seq_length, input_size)
    Y_seq = np.sum(X_seq, axis=1, keepdims=True)  # Simple regression target

    rnn = SimpleRNNBPTT(input_size, hidden_size, output_size, seq_length, learning_rate=0.05)
    rnn.train(X_seq, Y_seq, epochs=500, verbose=100)
