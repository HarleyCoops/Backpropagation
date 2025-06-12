🧠 Backpropagation Museum Project

## What is This?

Welcome to the Backpropagation Museum — a living, interactive homage to one of the most important algorithms in the history of artificial intelligence: Backpropagation and its extension, Backpropagation Through Time (BPTT).

This project is both a technical implementation and a digital museum. It brings together:
- The original Werbos BPTT paper in LaTeX (BP.tex)
- A modern, readable summary (BP_review.md)
- Faithful, well-documented NumPy code for BPTT (bptt_numpy.py)
- An advanced MCP server (mcp_server.py) that enables LLM-powered code generation, LaTeX-to-code conversion, and web search
- Setup scripts, configuration, and a vision for educational, historical, and technical exploration

---

## Why a Museum?

Backpropagation is the algorithm that made deep learning possible. BPTT extended it to recurrent neural networks, enabling machines to learn from sequences and time. This project is a tribute to the pioneers, a resource for learners, and a toolkit for researchers.

We are "sapiens paying homage to the emerging consciousness in AI."
Explore, learn, and help tell the story.

---

## 🚀 Quick Start

1. Clone the Repository

    git clone <your-repo-url>
    cd Backpropagation

2. Setup the Environment (Windows/PowerShell)

    pwsh setup.ps1

    - Installs dependencies in a virtual environment
    - Sets up config files and directories
    - Tests the MCP server and Jupyter kernel

3. Edit Configuration

    - Open .env (copied from config.env)
    - Add your OpenAI and Anthropic API keys for LLM-powered features

4. Run the MCP Server

    python mcp_server.py

    - Visit http://localhost:8000/health for status
    - The server exposes endpoints for LLM tools, LaTeX-to-code, and more

5. Explore the BPTT Implementation

    python bptt_numpy.py

    - Trains a simple RNN using BPTT on a toy sequence
    - See bptt_numpy.py for code, comments, and usage

---

## 🏛️ Project Structure

    BP_review.md                # Modern summary of BPTT
    BP.tex                      # Original Werbos BPTT paper (LaTeX)
    bptt_numpy.py               # NumPy implementation of BPTT
    mcp_server.py               # FastAPI MCP server with LLM/LaTeX tools
    requirements.txt            # Python dependencies
    setup.ps1                   # PowerShell setup script
    config.env / .env           # Environment variables (API keys, config)
    implementation-plan.txt     # Project plan
    instructions.txt            # Project instructions and vision
    Werbos-Backpropagation20through20time.pdf # Reference PDF

---

## 📚 Key Files

- BP.tex: The original, full LaTeX source of Werbos's "Backpropagation Through Time" paper, with equations, pseudocode, and references.
- BP_review.md: A modern, master's-level summary of BPTT, with clear explanations and mathematical insights.
- bptt_numpy.py: Faithful NumPy implementation of BPTT for a simple RNN, with comments and references to the original paper.
- mcp_server.py: FastAPI-based MCP server exposing:
    - Web and arXiv search tools
    - OpenAI/Anthropic code generation
    - LaTeX-to-code conversion
    - Resource access for project files

---

## 🧑‍💻 How to Contribute

- Fork the repo, make improvements, and submit a pull request.
- Ideas: Add new educational notebooks, visualizations, or interactive demos. Improve the BPTT implementation. Expand the museum with more historical context or modern research.

---

## 💡 Inspiration

"Backpropagation is the most important algorithm in AI."
— Geoffrey Hinton

This project is a tribute to the pioneers and a resource for the next generation of learners and builders.

---

## 📜 License

MIT License. See LICENSE file.

---

## 👀 See Also

- Werbos, P.J. "Backpropagation Through Time: What It Does and How to Do It" (IEEE, 1990)
- Original 1990 Paper (PDF): Werbos-Backpropagation20through20time.pdf

---
