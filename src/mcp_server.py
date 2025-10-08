"""MCP Server implementation with tools."""

import asyncio
import json
import logging
from typing import Any, Dict, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from src.tools import MCPTools, TOOL_DEFINITIONS
from src.config import MCP_SERVER_NAME, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPServerApp:
    """MCP Server application."""

    def __init__(self):
        self.server = Server(MCP_SERVER_NAME)
        self.tools = MCPTools()
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup request handlers for the MCP server."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools."""
            logger.info("Listing available tools")
            tools = []
            for tool_def in TOOL_DEFINITIONS:
                tools.append(Tool(
                    name=tool_def["name"],
                    description=tool_def["description"],
                    inputSchema=tool_def["inputSchema"]
                ))
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
            """Execute a tool with given arguments."""
            logger.info(f"Calling tool: {name} with arguments: {arguments}")

            try:
                # Route to appropriate tool method
                if name == "calculator":
                    result = self.tools.calculator(arguments.get("expression", ""))
                elif name == "get_current_time":
                    result = self.tools.get_current_time()
                elif name == "list_files":
                    result = self.tools.list_files(arguments.get("directory", "."))
                elif name == "read_file":
                    result = self.tools.read_file(
                        arguments.get("file_path", ""),
                        arguments.get("max_lines", 100)
                    )
                elif name == "write_file":
                    result = self.tools.write_file(
                        arguments.get("file_path", ""),
                        arguments.get("content", "")
                    )
                elif name == "system_info":
                    result = self.tools.system_info()
                elif name == "execute_command":
                    result = self.tools.execute_command(arguments.get("command", ""))
                else:
                    result = {
                        "success": False,
                        "error": f"Unknown tool: {name}"
                    }

                logger.info(f"Tool {name} result: {result}")

                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": str(e)
                    }, indent=2)
                )]

    async def run(self):
        """Run the MCP server."""
        logger.info(f"Starting MCP Server: {MCP_SERVER_NAME}")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for the MCP server."""
    server_app = MCPServerApp()
    await server_app.run()


if __name__ == "__main__":
    asyncio.run(main())

