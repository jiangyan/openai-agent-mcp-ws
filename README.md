# OpenAI Agents MCP WebSocket Example

This project demonstrates a simple client-server communication implementation using the Model Context Protocol (MCP) over WebSockets. It showcases how to build AI agents that can interact with tools provided by MCP servers.

## What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs (Large Language Models). It enables AI models to integrate with various data sources and tools, offering:

- A growing list of pre-built integrations for LLMs
- Flexibility to switch between LLM providers and vendors
- Best practices for securing data within your infrastructure

Think of MCP like a USB-C port for AI applications, providing a standardized way to connect AI models to different services and tools.

For example, we can use 2 simple mcp tool methods draw_dot (returns *) and draw_dash (returns ~) to draw morse codes, 😎
<img width="457" alt="image" src="https://github.com/user-attachments/assets/a0de038d-c988-4dfa-8264-cb2eaa7a6057" />

![image](https://github.com/user-attachments/assets/47c2a2f2-2ac1-48c3-8671-5ad2a34e3f09)

## Check your agent workflow in openai API platform's traces
<img width="1463" alt="image" src="https://github.com/user-attachments/assets/da459f92-56b8-40bd-9625-2bd12261149a" />

## Project Structure

- `server.py`: Implements a simple MCP server with two tools (`draw_dot` and `draw_dash`) exposed via WebSockets
- `client.py`: Implements an MCP client that uses OpenAI Agents to connect to the server and interact with its tools
- `pyproject.toml`: Defines project dependencies

## Prerequisites

- Python 3.10 or higher
- uv package manager
- An OpenAI API key

## Setup Instructions

1. Clone this repository:
```bash
git clone [repository-url]
cd openai-agent-mcp-ws
```

2. Set up your environment with uv:
```bash
# Install uv if you don't have it already
pip install uv

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here  # On Windows: set OPENAI_API_KEY=your_api_key_here
```

## Running the Example

1. Start the MCP server in one terminal:
```bash
uv run server.py
```

2. In another terminal, run the client:
```bash
uv run client.py
```

3. The client will prompt you to enter a question. The AI agent will use the tools provided by the server to respond.

4. Type `quit` to exit the client.

## How It Works

1. The server exposes two simple tools (`draw_dot` and `draw_dash`) through the MCP protocol over WebSockets
2. The client connects to the server and makes these tools available to an OpenAI Agent
3. When you ask a question, the Agent decides which tools to use and calls them through the MCP protocol
4. The server processes the tool calls and returns results, which the Agent uses to formulate a response
5. **IMPORTANT:** This demo does not implement a ping/pong keep-alive scheme for the WebSocket connection. As a result, the WebSocket connection may close after a few seconds of inactivity. Please be aware of this limitation when using the demo.

### MCPServerWs Wrapper

A key component of this implementation is the `MCPServerWs` wrapper class in `client.py`. This class:

- Wraps the MCP `ClientSession` to provide an interface compatible with OpenAI Agents
- Handles communication between the OpenAI Agent and the MCP server
- Provides methods to list available tools and call them
- Translates between the OpenAI Agents format and the MCP protocol

The wrapper implements three main methods:
- `list_tools()`: Retrieves the available tools from the MCP server
- `call_tool(name, arguments)`: Calls a specific tool on the MCP server with provided arguments
- `close()`: Properly closes the underlying session

This wrapper pattern allows the OpenAI Agents framework to seamlessly interact with any MCP-compatible server without needing to understand the details of the MCP protocol.

## Tracing

This example uses OpenAI's tracing capabilities. When you run the client, it will provide a URL to view the trace of the conversation in the OpenAI platform.

## Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/introduction)
- [OpenAI Agents Documentation](https://platform.openai.com/docs/agents/overview)

## License

[Do whatever you want]
