#!/usr/bin/env python3
"""MCP Client implementation with Ollama integration."""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional

import ollama

from src.config import OLLAMA_HOST, OLLAMA_MODEL, LOG_LEVEL
from src.tools import MCPTools, TOOL_DEFINITIONS

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPClient:
    """MCP Client with Ollama LLM integration."""

    def __init__(self):
        self.mcp_tools = MCPTools()
        self.tools: List[Dict[str, Any]] = []
        self.ollama_client = ollama.Client(host=OLLAMA_HOST)
        self.conversation_history: List[Dict[str, Any]] = []

    async def connect(self):
        """
        Initialize the MCP client and load tools.
        """
        logger.info("Initializing MCP client with local tools")

        # Load available tools
        await self._load_tools()

        logger.info("MCP client initialized")

    async def _load_tools(self):
        """Load available tools from tool definitions."""
        logger.info("Loading tools")

        # Convert tool definitions to Ollama format
        self.tools = []
        for tool_def in TOOL_DEFINITIONS:
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool_def["name"],
                    "description": tool_def["description"],
                    "parameters": tool_def["inputSchema"]
                }
            }
            self.tools.append(ollama_tool)

        logger.info(f"Loaded {len(self.tools)} tools: {[t['function']['name'] for t in self.tools]}")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool directly.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        logger.info(f"Calling tool: {tool_name} with arguments: {arguments}")

        try:
            # Route to appropriate tool method
            if tool_name == "calculator":
                result = self.mcp_tools.calculator(arguments.get("expression", ""))
            elif tool_name == "get_current_time":
                result = self.mcp_tools.get_current_time()
            elif tool_name == "list_files":
                result = self.mcp_tools.list_files(arguments.get("directory", "."))
            elif tool_name == "read_file":
                result = self.mcp_tools.read_file(
                    arguments.get("file_path", ""),
                    arguments.get("max_lines", 100)
                )
            elif tool_name == "write_file":
                result = self.mcp_tools.write_file(
                    arguments.get("file_path", ""),
                    arguments.get("content", "")
                )
            elif tool_name == "create_directory":
                result = self.mcp_tools.create_directory(arguments.get("directory_path", ""))
            elif tool_name == "system_info":
                result = self.mcp_tools.system_info()
            elif tool_name == "execute_command":
                result = self.mcp_tools.execute_command(arguments.get("command", ""))
            else:
                result = {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

            return result

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
        """Close the MCP client."""
        logger.info("MCP client closed")

