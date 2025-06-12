#!/usr/bin/env python3
"""
MCP Server for Backpropagation Museum Project
Enables internet access and integration with OpenAI Codex
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import aiohttp
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config.env")

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    """MCP protocol request model"""
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None

class MCPResponse(BaseModel):
    """MCP protocol response model"""
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class BackpropagationMCPServer:
    """MCP Server for Backpropagation implementation with internet access"""
    
    def __init__(self):
        self.app = FastAPI(title="Backpropagation MCP Server")
        self.setup_cors()
        self.setup_routes()
        
        # Initialize OpenAI client
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Internet access configuration
        self.internet_enabled = os.getenv("ENABLE_INTERNET_ACCESS", "false").lower() == "true"
        self.allowed_domains = os.getenv("ALLOWED_DOMAINS", "").split(",")
        self.max_requests_per_minute = int(os.getenv("MAX_NETWORK_REQUESTS_PER_MINUTE", "60"))
        
        logger.info(f"MCP Server initialized with internet access: {self.internet_enabled}")

    def setup_cors(self):
        """Setup CORS middleware for web access"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self):
        """Setup MCP protocol routes"""
        
        @self.app.post("/mcp")
        async def handle_mcp_request(request: MCPRequest):
            """Handle MCP protocol requests"""
            try:
                result = await self.process_mcp_request(request)
                return MCPResponse(result=result, id=request.id)
            except Exception as e:
                logger.error(f"MCP request error: {str(e)}")
                return MCPResponse(
                    error={"code": -1, "message": str(e)}, 
                    id=request.id
                )

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "internet_access": self.internet_enabled}

        @self.app.get("/capabilities")
        async def get_capabilities():
            """Return server capabilities"""
            return {
                "internet_access": self.internet_enabled,
                "allowed_domains": self.allowed_domains,
                "backpropagation_tools": True,
                "latex_processing": True,
                "openai_integration": bool(os.getenv("OPENAI_API_KEY"))
            }

    async def process_mcp_request(self, request: MCPRequest) -> Dict[str, Any]:
        """Process MCP protocol requests"""
        method = request.method
        params = request.params or {}
        
        if method == "tools/list":
            return await self.list_tools()
        elif method == "tools/call":
            return await self.call_tool(params)
        elif method == "resources/list":
            return await self.list_resources()
        elif method == "resources/read":
            return await self.read_resource(params)
        else:
            raise ValueError(f"Unknown method: {method}")

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            {
                "name": "web_search",
                "description": "Search the web for information about backpropagation and neural networks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 10}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "arxiv_search",
                "description": "Search arXiv for academic papers related to backpropagation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 5}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "generate_backprop_code",
                "description": "Generate backpropagation implementation code using OpenAI Codex",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "framework": {"type": "string", "enum": ["numpy", "pytorch", "tensorflow"], "default": "numpy"},
                        "complexity": {"type": "string", "enum": ["simple", "advanced"], "default": "simple"}
                    }
                }
            },
            {
                "name": "latex_to_code",
                "description": "Convert LaTeX mathematical expressions to executable code",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "latex_content": {"type": "string", "description": "LaTeX mathematical expression"},
                        "target_language": {"type": "string", "enum": ["python", "numpy", "pytorch"], "default": "python"}
                    },
                    "required": ["latex_content"]
                }
            }
        ]
        
        return {"tools": tools}

    async def call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "web_search":
            return await self.web_search(arguments)
        elif tool_name == "arxiv_search":
            return await self.arxiv_search(arguments)
        elif tool_name == "generate_backprop_code":
            return await self.generate_backprop_code(arguments)
        elif tool_name == "latex_to_code":
            return await self.latex_to_code(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def web_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Perform web search with internet access"""
        if not self.internet_enabled:
            raise ValueError("Internet access is disabled")
        
        query = args.get("query", "")
        max_results = args.get("max_results", 10)
        
        # This is a simplified implementation - in practice you'd use a proper search API
        async with aiohttp.ClientSession() as session:
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
            
            try:
                async with session.get(search_url) as response:
                    data = await response.json()
                    
                    results = []
                    for item in data.get("RelatedTopics", [])[:max_results]:
                        if "Text" in item and "FirstURL" in item:
                            results.append({
                                "title": item.get("Text", "")[:100],
                                "url": item.get("FirstURL", ""),
                                "snippet": item.get("Text", "")
                            })
                    
                    return {"results": results}
            except Exception as e:
                logger.error(f"Web search error: {str(e)}")
                return {"error": str(e), "results": []}

    async def arxiv_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search arXiv for academic papers"""
        if not self.internet_enabled:
            raise ValueError("Internet access is disabled")
        
        query = args.get("query", "")
        max_results = args.get("max_results", 5)
        
        # arXiv API search
        arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(arxiv_url) as response:
                    content = await response.text()
                    # Parse XML response (simplified)
                    return {"arxiv_results": content[:1000]}  # Truncated for brevity
            except Exception as e:
                logger.error(f"arXiv search error: {str(e)}")
                return {"error": str(e)}

    async def generate_backprop_code(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate backpropagation code using OpenAI Codex"""
        framework = args.get("framework", "numpy")
        complexity = args.get("complexity", "simple")
        
        prompt = f"""
        Generate a {complexity} backpropagation implementation using {framework}.
        Include forward pass, backward pass, and gradient calculation.
        Add comprehensive comments explaining each step.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in neural networks and backpropagation. Generate clean, well-commented code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            code = response.choices[0].message.content
            return {"generated_code": code, "framework": framework, "complexity": complexity}
            
        except Exception as e:
            logger.error(f"Code generation error: {str(e)}")
            return {"error": str(e)}

    async def latex_to_code(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Convert LaTeX mathematical expressions to code"""
        latex_content = args.get("latex_content", "")
        target_language = args.get("target_language", "python")
        
        prompt = f"""
        Convert this LaTeX mathematical expression to executable {target_language} code:
        
        {latex_content}
        
        Provide the code with clear variable names and comments.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert at converting mathematical expressions to {target_language} code."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            code = response.choices[0].message.content
            return {"converted_code": code, "source_latex": latex_content, "target_language": target_language}
            
        except Exception as e:
            logger.error(f"LaTeX conversion error: {str(e)}")
            return {"error": str(e)}

    async def list_resources(self) -> Dict[str, Any]:
        """List available resources"""
        resources = [
            {
                "uri": "file://BP.tex",
                "name": "Backpropagation Paper (LaTeX)",
                "description": "Original backpropagation paper in LaTeX format"
            },
            {
                "uri": "file://BP_review.md",
                "name": "Backpropagation Review",
                "description": "Review and summary of the backpropagation paper"
            },
            {
                "uri": "file://Werbos-Backpropagation20through20time.pdf",
                "name": "Werbos Backpropagation Through Time",
                "description": "Historical paper on backpropagation through time"
            }
        ]
        
        return {"resources": resources}

    async def read_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific resource"""
        uri = params.get("uri", "")
        
        if uri.startswith("file://"):
            filename = uri[7:]  # Remove "file://" prefix
            filepath = Path(filename)
            
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return {"content": content, "uri": uri}
                except Exception as e:
                    return {"error": f"Failed to read file: {str(e)}"}
            else:
                return {"error": f"File not found: {filename}"}
        else:
            return {"error": f"Unsupported URI scheme: {uri}"}

# Global server instance
server = BackpropagationMCPServer()
app = server.app

if __name__ == "__main__":
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    logger.info(f"Starting Backpropagation MCP Server on {host}:{port}")
    
    uvicorn.run(
        "mcp_server:app",
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("MCP_SERVER_LOG_LEVEL", "info").lower()
    ) 