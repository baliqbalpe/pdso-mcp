#!/usr/bin/env python3
"""MCP Client implementation with proper MCP protocol over STDIO."""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.config import OLLAMA_HOST, OLLAMA_MODEL, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPClient:
    """MCP Client that communicates with MCP Server via STDIO and integrates with Ollama LLM."""

    def __init__(self):
        self.tools: List[Dict[str, Any]] = []
        self.ollama_client = ollama.Client(host=OLLAMA_HOST)
        self.conversation_history: List[Dict[str, Any]] = []
        self.session: Optional[ClientSession] = None
        self._server_params: Optional[StdioServerParameters] = None
        self._read_stream = None
        self._write_stream = None
        self._stdio_context = None
        self._session_context = None

    async def connect(self):
        """
        Initialize the MCP client by spawning the MCP server and connecting via STDIO.
        """
        logger.info("Initializing MCP client - spawning MCP server subprocess")

        # Get the project root directory
        project_root = Path(__file__).parent.parent
        server_script = project_root / "src" / "mcp_server.py"

        # Configure server parameters for STDIO communication
        self._server_params = StdioServerParameters(
            command="python3",
            args=[str(server_script)],
            env=None
        )

        logger.info(f"Starting MCP server: python3 {server_script}")

        # Connect to server via STDIO
        try:
            self._stdio_context = stdio_client(self._server_params)
            self._read_stream, self._write_stream = await self._stdio_context.__aenter__()

            # Create client session
            self._session_context = ClientSession(self._read_stream, self._write_stream)
            self.session = await self._session_context.__aenter__()

            # Initialize the session (MCP handshake)
            logger.info("Initializing MCP session")
            await self.session.initialize()

            logger.info("MCP session initialized successfully")

            # Discover tools from the MCP server
            await self._load_tools()

            logger.info("MCP client connected and ready")

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            await self.close()
            raise

    async def _load_tools(self):
        """Discover tools from the MCP server via list_tools() call."""
        logger.info("Discovering tools from MCP server")

        try:
            # Call MCP server's list_tools
            tools_result = await self.session.list_tools()

            # Convert MCP Tool format to Ollama format
            self.tools = []
            for tool in tools_result.tools:
                ollama_tool = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                }
                self.tools.append(ollama_tool)

            tool_names = [t['function']['name'] for t in self.tools]
            logger.info(f"Discovered {len(self.tools)} tools from MCP server: {tool_names}")

        except Exception as e:
            logger.error(f"Failed to load tools from MCP server: {e}")
            raise

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool via the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        logger.info(f"Calling tool via MCP: {tool_name} with arguments: {arguments}")

        try:
            # Call tool via MCP protocol
            result = await self.session.call_tool(tool_name, arguments)

            # Parse the result - MCP returns list of TextContent
            if result.content and len(result.content) > 0:
                # Get the first content item (should be JSON)
                content_item = result.content[0]
                if hasattr(content_item, 'text'):
                    # Parse JSON response
                    tool_result = json.loads(content_item.text)
                    return tool_result
                else:
                    return {"success": False, "error": "Unexpected content format"}
            else:
                return {"success": False, "error": "No content in tool response"}

        except Exception as e:
            logger.error(f"Error calling tool {tool_name} via MCP: {e}")
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

                # Execute each tool call via MCP
                for tool_call in assistant_message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]

                    logger.info(f"Executing tool via MCP: {tool_name}")
                    print(f"\n[Calling tool via MCP: {tool_name}]")

                    # Execute tool via MCP server
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
        """Close the MCP client and server connection."""
        logger.info("Closing MCP client")

        try:
            # Close session context
            if self._session_context and self.session:
                await self._session_context.__aexit__(None, None, None)
                self.session = None

            # Close STDIO context (this will terminate the server subprocess)
            if self._stdio_context:
                await self._stdio_context.__aexit__(None, None, None)

            logger.info("MCP client closed successfully")
        except Exception as e:
            logger.error(f"Error closing MCP client: {e}")
