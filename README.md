# MCP Client & Server with Local LLM

A complete implementation of Model Context Protocol (MCP) client and server with local LLM integration using Ollama. This project provides an interactive CLI interface for chatting with a local language model that can use various tools through MCP.

## 🌟 Features

- **Full MCP Implementation**: Complete client and server implementation
- **Local LLM Integration**: Uses Ollama for running local language models (Llama 3.2, Mistral, etc.)
- **Interactive CLI**: Rich terminal interface for chatting with the LLM
- **Multiple Tools**: Pre-built tools for file operations, calculations, system info, and more
- **Cloud Ready**: Designed to run on cloud machines with easy setup

## 🛠️ Available Tools

The MCP server provides the following tools:

1. **calculator** - Evaluate mathematical expressions
2. **get_current_time** - Get current date and time with timezone
3. **list_files** - List files and directories
4. **read_file** - Read file contents
5. **write_file** - Write content to files
6. **system_info** - Get system information
7. **execute_command** - Execute shell commands (use with caution)

## 📋 Prerequisites

- Python 3.8 or higher
- Linux/macOS (for cloud deployment)
- At least 4GB RAM for running local LLM models

## 🚀 Quick Start

### 1. Clone or Upload to Your Cloud Machine

```bash
# Upload this directory to your cloud machine
# Or clone if it's in a git repository
```

### 2. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
1. Create a Python virtual environment
2. Install all dependencies
3. Install and configure Ollama
4. Pull the Llama 3.2 model (3B parameters)
5. Create necessary directories and config files

### 3. Start the Client

```bash
chmod +x start.sh
./start.sh
```

Or manually:

```bash
source venv/bin/activate
python main.py
```

## 💬 Using the CLI

Once started, you'll see an interactive chat interface:

```
╭─────────────────────────────────────────╮
│ MCP Client with Local LLM               │
│ Using model: llama3.2:3b                │
│ Type your messages and press Enter.     │
│ Type 'exit' or 'quit' to stop.         │
│ Type 'reset' to clear conversation.     │
╰─────────────────────────────────────────╯

Available tools: calculator, get_current_time, list_files, ...

You: What time is it?
```

### Commands

- Type your message and press Enter to chat
- `exit` or `quit` - Exit the application
- `reset` - Clear conversation history
- `Ctrl+C` - Interrupt current operation

### Example Interactions

1. **Using Calculator Tool**:
   ```
   You: What is 15 * 23 + 100?

   [Calling tool: calculator]

   Assistant: The result is 445.
   ```

2. **Getting Time**:
   ```
   You: What's the current time?

   [Calling tool: get_current_time]

   Assistant: The current time is 14:30:45 on Wednesday, October 8, 2025.
   ```

3. **File Operations**:
   ```
   You: List the files in the current directory

   [Calling tool: list_files]

   Assistant: Here are the files in the current directory:
   - main.py (file)
   - requirements.txt (file)
   - src/ (directory)
   ...
   ```

4. **System Information**:
   ```
   You: What system am I running on?

   [Calling tool: system_info]

   Assistant: You're running on Linux with Python 3.10.12...
   ```

## 📁 Project Structure

```
mcp/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── tools.py             # MCP server tools
│   ├── mcp_server.py        # MCP server implementation
│   ├── mcp_client.py        # MCP client with Ollama integration
│   └── cli.py               # Interactive CLI interface
├── data/                    # Data directory for file operations
├── main.py                  # Main entry point
├── setup.sh                 # Setup script
├── start.sh                 # Start script
├── test_server.py           # Tool testing script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (created by setup)
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## ⚙️ Configuration

Configuration is managed through environment variables in the `.env` file:

```bash
# MCP Configuration
MCP_SERVER_NAME=local-mcp-server
MCP_CLIENT_NAME=local-mcp-client

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Logging
LOG_LEVEL=INFO
```

### Changing the LLM Model

To use a different model:

1. Pull the model:
   ```bash
   ollama pull mistral:latest
   ```

2. Update `.env`:
   ```bash
   OLLAMA_MODEL=mistral:latest
   ```

3. Restart the client

### Available Models

- `llama3.2:3b` - Small, fast model (recommended for 4GB RAM)
- `llama3.2:1b` - Tiny model for limited resources
- `mistral:latest` - Alternative model with good performance
- `llama3:8b` - Larger model (requires 8GB+ RAM)

## 🧪 Testing

Test the MCP server tools:

```bash
python test_server.py
```

This will test all available tools and show their outputs.

## 📊 System Requirements

### Minimum
- 2 CPU cores
- 4GB RAM
- 10GB disk space

### Recommended
- 4+ CPU cores
- 8GB+ RAM
- 20GB+ disk space

### Model Size Guide

| Model | RAM Required | Speed | Quality |
|-------|-------------|-------|---------|
| llama3.2:1b | 2GB | Very Fast | Basic |
| llama3.2:3b | 4GB | Fast | Good |
| llama3:8b | 8GB | Medium | Excellent |
| mistral:latest | 6GB | Medium | Very Good |

## 🔧 Troubleshooting

### Ollama Service Not Starting

```bash
# Check if Ollama is running
pgrep -x ollama

# Start Ollama manually
ollama serve &
```

### Model Not Found

```bash
# Pull the model again
ollama pull llama3.2:3b
```

### Connection Issues

Check if the Ollama service is accessible:

```bash
curl http://localhost:11434/api/tags
```

### Python Module Errors

Make sure the virtual environment is activated:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## 📝 Development

### Adding New Tools

1. Add the tool method to `MCPTools` class in `src/tools.py`
2. Add the tool definition to `TOOL_DEFINITIONS` list
3. Add the routing logic in `src/mcp_server.py`

Example:

```python
# In src/tools.py
@staticmethod
def my_new_tool(param: str) -> Dict[str, Any]:
    """My new tool description."""
    return {"success": True, "result": param.upper()}

# Add to TOOL_DEFINITIONS
{
    "name": "my_new_tool",
    "description": "Description of what the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
}
```

## 🔐 Security Notes

- The `execute_command` tool can run arbitrary shell commands. Use with caution.
- When deploying to cloud, ensure proper firewall rules
- Consider removing dangerous tools in production environments
- Never expose the MCP server directly to the internet without authentication

## 📄 License

This project is open source and available for use and modification.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📚 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Ollama Documentation](https://ollama.com/docs)
- [Ollama Model Library](https://ollama.com/library)

## 💡 Tips

1. Start with smaller models first to ensure everything works
2. Use `reset` command to clear context and save memory
3. The LLM decides when to use tools based on their descriptions
4. More detailed tool descriptions lead to better tool usage
5. Monitor system resources when running larger models

## 🎯 Next Steps

1. Customize tools for your specific use case
2. Add more specialized tools (API calls, database access, etc.)
3. Integrate with other services
4. Build automation workflows using the tools
5. Create custom prompts and agents

---

Built with ❤️ using MCP and Ollama

