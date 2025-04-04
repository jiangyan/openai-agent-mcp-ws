import asyncio
from typing import Any

import uvicorn
from mcp.server.websocket import websocket_server
from starlette.applications import Starlette
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("SimpleWebSocketServer")

@mcp.tool()
async def draw_dot(arguments: dict | None) -> str:
    """draw a dot and returns"""
    return "*"

@mcp.tool()
async def draw_dash(arguments: dict | None) -> str:
    """draw a dash and returns"""
    return "~"


# Define the ASGI WebSocket endpoint
async def mcp_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for the MCP server."""
    try:
        async with websocket_server(websocket.scope, websocket.receive, websocket.send) as (read_stream, write_stream):            
            init_options = mcp._mcp_server.create_initialization_options()
            await mcp._mcp_server.run(read_stream, write_stream, init_options)
            
    except Exception:
        await websocket.close()


# Create the Starlette ASGI application with the WebSocket route
app = Starlette(routes=[
    WebSocketRoute("/mcp", endpoint=mcp_endpoint)
])

async def main():
    """Runs the Uvicorn server."""
    config = uvicorn.Config(app, host="localhost", port=8000,log_level="info")
    server = uvicorn.Server(config)
    print("Starting WebSocket MCP server on ws://localhost:8000/mcp")
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.") 