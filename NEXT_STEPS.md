# Next Steps

This repository aims to become an interactive "Backpropagation Museum". Below are concrete steps to advance the project and ensure the MCP server and Claude/Codex integrations are fully operational.

## 1. Configure the Environment
- Edit `config.env` with valid OpenAI and Anthropic API keys.
- Set `MCP_SERVER_HOST` to your E2B machine's address and confirm `MCP_SERVER_PORT` and `MCP_SERVER_LOG_LEVEL`.
- Keep `ENABLE_INTERNET_ACCESS=true` so the server's tools can reach the web.

## 2. Install Dependencies
- On your E2B instance, clone this repository and run:
  ```bash
  pip install -r requirements.txt
  ```
- Ensure heavy libraries like NumPy, matplotlib, and torch install successfully so tests do not fail.

## 3. Launch the MCP Server
- Start the server using:
  ```bash
  python mcp_server.py
  ```
- The main block in `mcp_server.py` starts Uvicorn using the host and port from `config.env`:
  ```python
  host = os.getenv("MCP_SERVER_HOST", "localhost")
  port = int(os.getenv("MCP_SERVER_PORT", "8000"))
  uvicorn.run(
      "mcp_server:app",
      host=host,
      port=port,
      reload=True,
      log_level=os.getenv("MCP_SERVER_LOG_LEVEL", "info").lower()
  )
  ```

## 4. Verify Codex and Claude Access
- With the server running, call the `generate_backprop_code` tool for a simple test of Codex.
- Use the `ANTHROPIC-CHAT` tool to send an instruction to Claude. An example request is detailed in `E2B_Anthropic_MCP_Usage.txt`:
  ```bash
  curl -X POST http://<E2B_SERVER_HOST>:<PORT>/mcp \
    -H "Content-Type: application/json" \
    -d '{
          "method": "tools/call",
          "params": {
              "name": "ANTHROPIC-CHAT",
              "arguments": {
                  "instruction": "Write a haiku about neural networks."
              }
          }
        }'
  ```
- A JSON response confirms that Claude is reachable.

## 5. Build the Backpropagation Museum
- Implement the NumPy version of Backpropagation Through Time as outlined in `implementation-plan.txt`:
  - Extract equations from `BP.tex` and `BP_review.md`.
  - Write a well-commented implementation and (optionally) a demonstration notebook.
- Create educational diagrams or animations to illustrate gradient flow through time.

## 6. Document Everything
- Expand the README with examples and links to any notebooks or visualizations.
- Provide usage instructions for both Codex and Claude tools so collaborators can reproduce your setup.

Following these steps will establish a functioning MCP server on E2B with both Codex and Claude integration, paving the way for the "epic illustration" of the backpropagation algorithm.
