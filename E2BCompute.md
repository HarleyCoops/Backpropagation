1. Configure Environment
Edit config.env to specify your server details. The file already provides variables for the host and port (lines 8‑11) and allows toggling internet access (lines 13‑16):

 8  # MCP Server Configuration
 9  MCP_SERVER_HOST=localhost
10  MCP_SERVER_PORT=8000
11  MCP_SERVER_LOG_LEVEL=INFO
...
13  # Agent Network Configuration
14  ENABLE_INTERNET_ACCESS=true
15  MAX_NETWORK_REQUESTS_PER_MINUTE=60
16  ALLOWED_DOMAINS=arxiv.org,scholar.google.com,github.com,wikipedia.org

Set MCP_SERVER_HOST to the E2B machine’s address and adjust the port if needed. Ensure internet access is enabled if you want the MCP tools (web search, arXiv search, etc.) to function.

2. Install Dependencies on E2B
Copy the repository to your E2B system and install the packages in requirements.txt. The MCP server relies on FastAPI, OpenAI, aiohttp, uvicorn, and other libraries defined there.

3. Launch the MCP Server
Run the server with:

python mcp_server.py
The main block (lines 348‑360 of mcp_server.py) starts uvicorn using the host and port from config.env:

348  if __name__ == "__main__":
349      host = os.getenv("MCP_SERVER_HOST", "localhost")
350      port = int(os.getenv("MCP_SERVER_PORT", "8000"))
...
354      uvicorn.run(
355          "mcp_server:app",
356          host=host,
357          port=port,
358          reload=True,
359          log_level=os.getenv("MCP_SERVER_LOG_LEVEL", "info").lower()
360      )

Once running on E2B, the server will expose endpoints like /mcp, /health, and /capabilities.

4. Connect to Codex / Claude
Provide your OpenAI and Anthropic API keys in config.env (lines 2‑6). The server loads these on startup:

23  # Load environment variables
24  load_dotenv("config.env")
...
53  # Initialize OpenAI client
54  openai.api_key = os.getenv("OPENAI_API_KEY")

With those keys set, you can call the server’s tools (e.g., generate_backprop_code) to leverage Codex.

5. Pipe Workloads to E2B
Because the server is just a FastAPI app, you can send HTTP requests from any client (local machine, CI/CD pipeline, etc.) to your E2B instance. If you need heavier computation (large model training), you can trigger those tasks via the server—either by extending the current tool set or by running scripts on E2B that the MCP server calls.

In summary, replicate the repo on your E2B environment, adjust config.env with the E2B host and keys, install dependencies, and run python mcp_server.py. Once running, you can send requests to that server from your local setup to take advantage of the compute power available on E2B.