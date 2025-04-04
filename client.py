import asyncio

from typing import Any, List
from mcp import ClientSession
from mcp.client.websocket import websocket_client

from agents import Agent, Runner, trace, gen_trace_id
from agents.model_settings import ModelSettings

# Define the wrapper class
class MCPServerWs:
    """Wraps mcp.ClientSession to provide Agent-compatible interface."""
    def __init__(self, session: ClientSession, name: str):
        self._session = session
        self.name = name

    async def list_tools(self) -> List[Any]:
        """Calls underlying session.list_tools and parses the response."""
        
        raw_response = await self._session.list_tools()
        
        tools = []
        if hasattr(raw_response, "tools") and isinstance(raw_response.tools, list):
            tools = raw_response.tools
        else:
            print("Warning - Unexpected list_tools response format.")
        print(f"Wrapper: Parsed tools: {tools}")
        return tools


    async def call_tool(self, name: str, arguments: dict | None) -> Any:
        """Delegates call_tool and returns the raw result."""
        print(f"Wrapper: call_tool({name}, {arguments})")
        raw_result = await self._session.call_tool(name, arguments)
        print(f"Wrapper: call_tool result: {raw_result}")        
        return raw_result

    async def close(self) -> None:
        """Delegates close to the underlying session."""
        
        if hasattr(self._session, "close"):
            await self._session.close()    


async def main():
    url = "ws://localhost:8000/mcp"
    try:
        async with websocket_client(url) as (read_stream, write_stream):
            print("WebSocket transport established.")
            async with ClientSession(read_stream, write_stream) as session:
                
                await session.initialize()
                mcp_server_ws = MCPServerWs(session, "SimpleWebSocketServer")

                agent = Agent(
                    name="Assistant",
                    instructions="Use the tools to answer the questions.",
                    mcp_servers=[mcp_server_ws], # Pass the wrapper
                    model_settings=ModelSettings(tool_choice="required"),
                )
                trace_id = gen_trace_id()
                with trace(workflow_name="Simple websocket server agent demo", trace_id=trace_id):
                    print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

                    # Interaction loop
                    while True:
                        message = input("Enter your question (or 'quit' to exit): ")
                        if message.lower() == "quit":
                            print("Exiting program...")
                            break
                        
                        result = await Runner.run(starting_agent=agent, input=message, max_turns=30)
                        print(result.final_output)

            print("MCP ClientSession context exited.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
