#!/usr/bin/env python3
"""MCP Server Tools - Collection of useful tools for the LLM."""

import os
import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class MCPTools:
    """Collection of tools that the MCP server will expose."""

    @staticmethod
    def calculator(expression: str) -> Dict[str, Any]:
        """
        Evaluate a mathematical expression.

        Args:
            expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")

        Returns:
            Dictionary with result or error
        """
        try:
            # Safe evaluation - only allows basic math operations
            result = eval(expression, {"__builtins__": {}}, {})
            return {
                "success": True,
                "result": result,
                "expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "expression": expression
            }

    @staticmethod
    def get_current_time() -> Dict[str, Any]:
        """
        Get the current date and time.

        Returns:
            Dictionary with current datetime information
        """
        now = datetime.now()
        return {
            "success": True,
            "datetime": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "timezone": datetime.now().astimezone().tzname()
        }

    @staticmethod
    def list_files(directory: str = ".") -> Dict[str, Any]:
        """
        List files and directories in a given path.

        Args:
            directory: Path to list (defaults to current directory)

        Returns:
            Dictionary with list of files and directories
        """
        try:
            path = Path(directory).expanduser()
            if not path.exists():
                return {
                    "success": False,
                    "error": f"Directory does not exist: {directory}"
                }

            items = []
            for item in path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None,
                    "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })

            return {
                "success": True,
                "directory": str(path.absolute()),
                "items": items,
                "count": len(items)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def read_file(file_path: str, max_lines: int = 100) -> Dict[str, Any]:
        """
        Read contents of a text file.

        Args:
            file_path: Path to the file to read
            max_lines: Maximum number of lines to read (default 100)

        Returns:
            Dictionary with file contents or error
        """
        try:
            path = Path(file_path).expanduser()
            if not path.exists():
                return {
                    "success": False,
                    "error": f"File does not exist: {file_path}"
                }

            if not path.is_file():
                return {
                    "success": False,
                    "error": f"Path is not a file: {file_path}"
                }

            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                content = ''.join(lines[:max_lines])

            return {
                "success": True,
                "file": str(path.absolute()),
                "content": content,
                "lines_read": min(len(lines), max_lines),
                "total_lines": len(lines),
                "truncated": len(lines) > max_lines
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def write_file(file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file.

        Args:
            file_path: Path to the file to write
            content: Content to write to the file

        Returns:
            Dictionary with operation result
        """
        try:
            path = Path(file_path).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "success": True,
                "file": str(path.absolute()),
                "bytes_written": len(content.encode('utf-8'))
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def system_info() -> Dict[str, Any]:
        """
        Get system information.

        Returns:
            Dictionary with system information
        """
        try:
            import platform

            return {
                "success": True,
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def execute_command(command: str) -> Dict[str, Any]:
        """
        Execute a shell command (use with caution).

        Args:
            command: Shell command to execute

        Returns:
            Dictionary with command output or error
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "success": result.returncode == 0,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out after 30 seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Tool definitions for MCP server
TOOL_DEFINITIONS = [
    {
        "name": "calculator",
        "description": "Evaluate a mathematical expression. Supports basic arithmetic operations like +, -, *, /, **, %",
        "inputSchema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time with timezone information",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "list_files",
        "description": "List files and directories in a given path",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Path to list (defaults to current directory)"
                }
            }
        }
    },
    {
        "name": "read_file",
        "description": "Read contents of a text file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                },
                "max_lines": {
                    "type": "integer",
                    "description": "Maximum number of lines to read (default 100)"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "system_info",
        "description": "Get system information including OS, hostname, and Python version",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "execute_command",
        "description": "Execute a shell command and return the output. Use with caution!",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute"
                }
            },
            "required": ["command"]
        }
    }
]

