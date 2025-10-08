"""MCP Client implementation with Ollama integration."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ollama

from src.config import OLLAMA_HOST, OLLAMA_MODEL, MCP_SERVER_NAME, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPClient:
    """MCP Client with Ollama LLM integration."""

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.tools: List[Dict[str, Any]] = []
        self.ollama_client = ollama.Client(host=OLLAMA_HOST)
        self.conversation_history: List[Dict[str, Any]] = []

    async def connect(self, server_script_path: str):
        """
        Connect to the MCP server.

        Args:
            server_script_path: Path to the MCP server script
        """
        logger.info(f"Connecting to MCP server: {server_script_path}")

        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )

        self.read_stream, self.write_stream = await stdio_client(server_params).__aenter__()
        self.session = await ClientSession(self.read_stream, self.write_stream).__aenter__()

        # Initialize session
        await self.session.initialize()
        logger.info("MCP session initialized")

        # Get available tools
        await self._load_tools()

    async def _load_tools(self):
        """Load available tools from the MCP server."""
        logger.info("Loading tools from MCP server")

        response = await self.session.list_tools()

        # Convert MCP tools to Ollama format
        self.tools = []
        for tool in response.tools:
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            self.tools.append(ollama_tool)

        logger.info(f"Loaded {len(self.tools)} tools: {[t['function']['name'] for t in self.tools]}")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")

        try:
            result = await self.session.call_tool(tool_name, arguments)

            # Extract text content from result
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return json.loads(content.text)

            return {"success": False, "error": "No content returned from tool"}

        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"success": False, "error": str(e)}

    async def chat(self, user_message: str) -> str:
        """
        Send a message to the LLM and handle tool calls.

        Args:
            user_message: User's message

        Returns:
            Assistant's response
        """
        logger.info(f"User message: {user_message}")

        # Add user message to conversation
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Call LLM with tools
        try:
            response = self.ollama_client.chat(
                model=OLLAMA_MODEL,
                messages=self.conversation_history,
                tools=self.tools
            )

            assistant_message = response.get("message", {})

            # Check if LLM wants to use tools
            if assistant_message.get("tool_calls"):
                logger.info(f"LLM requested {len(assistant_message['tool_calls'])} tool calls")

                # Add assistant's tool call request to history
                self.conversation_history.append(assistant_message)

                # Execute each tool call
                for tool_call in assistant_message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]

                    logger.info(f"Executing tool: {tool_name}")
                    print(f"\n[Calling tool: {tool_name}]")

                    # Execute tool via MCP
                    tool_result = await self.call_tool(tool_name, tool_args)

                    # Add tool result to conversation
                    self.conversation_history.append({
                        "role": "tool",
                        "content": json.dumps(tool_result)
                    })

                # Get final response from LLM after tool execution
                final_response = self.ollama_client.chat(
                    model=OLLAMA_MODEL,
                    messages=self.conversation_history
                )

                final_message = final_response["message"]
                self.conversation_history.append(final_message)

                return final_message["content"]

            else:
                # No tool calls, just return the response
                self.conversation_history.append(assistant_message)
                return assistant_message.get("content", "")

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")

    async def close(self):
        """Close the MCP connection."""
        if self.session:
            await self.session.__aexit__(None, None, None)
        logger.info("MCP client connection closed")

