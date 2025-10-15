# MCP Basic - Learning MCP with Local LLM

A complete implementation of Model Context Protocol (MCP) using local LLM with Ollama. This project showcases the full MCP architecture with proper client-server communication via JSON-RPC over STDIO - perfect for learning MCP fundamentals without API keys, runs entirely on your machine.

**Repository**: https://github.com/baliqbalpe/mcp-basic

---

## 🏗️ Architecture

This project implements the **full MCP protocol specification**:

```
┌─────────────────────────────────────────────────┐
│                    User                          │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│               CLI (cli.py)                       │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│         MCP Client (mcp_client.py)               │
│  ┌──────────────────────────────────────────┐   │
│  │  - Spawns MCP Server subprocess          │   │
│  │  - Connects via STDIO                    │   │
│  │  - Discovers tools (list_tools)          │   │
│  │  - Executes tools (call_tool)            │   │
│  │  - Integrates with Ollama for chat       │   │
│  └──────────────────────────────────────────┘   │
└───────────┬──────────────────┬──────────────────┘
            │                  │
            │ JSON-RPC         │ HTTP
            │ over STDIO       │
            ▼                  ▼
┌───────────────────┐   ┌──────────────────┐
│   MCP Server      │   │   Ollama LLM     │
│ (mcp_server.py)   │   │  (localhost)     │
│  ┌─────────────┐  │   └──────────────────┘
│  │list_tools() │  │
│  │call_tool()  │  │
│  └─────────────┘  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   MCPTools        │
│   (tools.py)      │
│  - calculator     │
│  - list_files     │
│  - read_file      │
│  - etc.           │
└───────────────────┘
```

### Key Components:

1. **MCP Client** - Acts as the MCP Host, spawns server, discovers tools dynamically
2. **MCP Server** - Standalone subprocess exposing tools via JSON-RPC over STDIO
3. **Transport Layer** - STDIO communication (standard MCP transport)
4. **Protocol** - JSON-RPC 2.0 with MCP message types
5. **LLM Integration** - Ollama for natural language interaction

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/baliqbalpe/mcp-basic.git
cd mcp-basic

# 2. Run automated setup
chmod +x setup.sh start.sh
./setup.sh

# 3. Start chatting!
./start.sh
```

That's it! The setup script installs everything automatically.

---

## 🌟 Features

- ✅ **Full MCP Protocol** - Complete JSON-RPC 2.0 over STDIO implementation
- ✅ **Client-Server Architecture** - Proper separation with subprocess communication
- ✅ **Dynamic Tool Discovery** - Tools discovered at runtime via `list_tools()`
- ✅ **8 Built-in Tools** - File operations, calculations, system info
- ✅ **Local LLM** - Runs Ollama models (Llama 3.2, Mistral) locally
- ✅ **Interactive CLI** - Beautiful terminal interface
- ✅ **No API Keys** - Completely private, runs offline
- ✅ **Cloud Ready** - Easy deployment on any Linux server
- ✅ **MCP Protocol** - Full Model Context Protocol implementation

---

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `calculator` | Evaluate math expressions |
| `get_current_time` | Get current date/time with timezone |
| `list_files` | List files and directories |
| `read_file` | Read file contents |
| `write_file` | Write content to files |
| `system_info` | Get OS, CPU, Python version |
| `execute_command` | Run shell commands |

---

## 📋 Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **Linux or macOS** (Windows with WSL2)
- **4GB RAM minimum** (8GB recommended)
- **10GB disk space** (for models)

---

## 📦 Tested Versions

This project has been tested with the following dependency versions to ensure stability:

### Core Dependencies
- **Python**: 3.8+ (recommended 3.10+)
- **pip**: 24.2
- **Ollama**: 0.3.x or later

### Python Packages (pinned in requirements.txt)
- **mcp**: 1.1.2
- **httpx**: 0.27.2
- **aiohttp**: 3.10.5
- **ollama**: 0.3.3
- **python-dotenv**: 1.0.1
- **click**: 8.1.7
- **rich**: 13.9.2
- **pydantic**: 2.9.2

**Last tested**: October 2025

> **Note**: All Python package versions are pinned in `requirements.txt` to prevent breaking changes. The setup script will install pip 24.2 and Ollama's latest stable version.

---

## 💻 Installation

```bash
git clone https://github.com/baliqbalpe/mcp-basic.git
cd mcp-basic
chmod +x setup.sh
./setup.sh
```

---

## 💬 Usage

### Starting the Client

```bash
./start.sh
```

Or manually:

```bash
source venv/bin/activate
python3 main.py
```

### Example Interactions

**Calculate Math:**
```
You: What is 15 * 23 + 100?
[Calling tool: calculator]
Assistant: The result is 445.
```

**Get Time:**
```
You: What time is it?
[Calling tool: get_current_time]
Assistant: It's currently 14:30:45 on Sunday, October 12, 2025.
```

**List Files:**
```
You: List files in the current directory
[Calling tool: list_files]
Assistant: Here are the files: main.py, requirements.txt, src/, data/...
```

**System Info:**
```
You: What system am I on?
[Calling tool: system_info]
Assistant: You're running Linux with Python 3.10.12...
```

### CLI Commands

- `exit` or `quit` - Exit the application
- `reset` - Clear conversation history
- `Ctrl+C` - Interrupt current operation

---

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Logging
LOG_LEVEL=INFO
```

### Available Models

```bash
# Smallest (2GB RAM)
ollama pull llama3.2:1b

# Recommended (4GB RAM)
ollama pull llama3.2:3b

# Better quality (8GB RAM)
ollama pull llama3:8b

# Alternative
ollama pull mistral:latest

# Update .env with your choice
nano .env  # Change OLLAMA_MODEL=your-model
```

---

## 📝 Command Reference

### Daily Use

```bash
# Start everything
./start.sh

# Or manually
cd /root/mcp-basic
source venv/bin/activate
python3 main.py
```

### Ollama Management

```bash
# Check if running
pgrep -x ollama

# Start Ollama
nohup ollama serve > ollama.log 2>&1 &

# Stop Ollama
pkill ollama

# List models
ollama list

# Pull a model
ollama pull llama3.2:3b

# Check logs
tail -f ollama.log
```

### Testing

```bash
# Test tools
python3 test_server.py

# Test Ollama
curl http://localhost:11434/api/tags
```

### Background Running

```bash
# Using tmux (recommended)
apt install -y tmux
tmux new -s mcp
python3 main.py
# Detach: Ctrl+B then D
# Reattach: tmux attach -t mcp

# Using screen
apt install -y screen
screen -S mcp
python3 main.py
# Detach: Ctrl+A then D
# Reattach: screen -r mcp
```

---

## 🔧 Troubleshooting

### MCP Server Connection Issues

```bash
# Check if server can run standalone
python3 src/mcp_server.py
# Should show: "Starting MCP Server" and wait for connections

# Check logs
# Look for "Client connected via STDIO" in logs
```

### Ollama Not Running

```bash
# Check status
pgrep -x ollama

# Start it
nohup ollama serve > ollama.log 2>&1 &
sleep 3
```

### Model Not Found

```bash
# Check installed models
ollama list

# Pull again
ollama pull llama3.2:3b
```

### Import Errors

```bash
# Check you're in project directory
pwd  # Should show: /root/mcp-basic

# Check venv is activated
which python3  # Should show: .../venv/bin/python3

# Reinstall dependencies
python3 -m pip install --force-reinstall -r requirements.txt
```

### Out of Memory

```bash
# Check memory
free -h

# Use smaller model
ollama pull llama3.2:1b
nano .env  # Change to OLLAMA_MODEL=llama3.2:1b
```

### After Reboot

```bash
cd /root/mcp-basic
source venv/bin/activate
nohup ollama serve > ollama.log 2>&1 &
sleep 3
python3 main.py
```

---

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

| Model | RAM | Speed | Quality |
|-------|-----|-------|---------|
| llama3.2:1b | 2GB | Very Fast | Basic |
| llama3.2:3b | 4GB | Fast | Good |
| llama3:8b | 8GB | Medium | Excellent |
| mistral:latest | 6GB | Medium | Very Good |

---

## 📁 Project Structure

```
mcp-basic/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── tools.py           # MCP tools implementation
│   ├── mcp_server.py      # MCP Server (STDIO, JSON-RPC)
│   ├── mcp_client.py      # MCP Client (spawns server, Ollama integration)
│   └── cli.py             # Interactive CLI
├── data/                  # Data directory
├── main.py                # Entry point
├── setup.sh               # Setup script
├── start.sh               # Start script
├── test_server.py         # Testing script
├── requirements.txt       # Dependencies
├── env.example            # Config template
└── README.md              # This file
```

---

## 🔐 Security Notes

- The `execute_command` tool can run shell commands - use carefully
- When deploying to cloud, configure firewall rules
- Consider removing dangerous tools in production
- Never expose MCP server to internet without authentication

---

## 🛠️ Development

### Adding New Tools

1. Add tool method to `MCPTools` class in `src/tools.py`
2. Add tool definition to `TOOL_DEFINITIONS` in `src/tools.py`
3. Add routing in `src/mcp_server.py` `call_tool()` handler

**That's it!** The client will automatically discover the new tool via the MCP protocol.

Example:

```python
# In src/tools.py
@staticmethod
def my_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    return {"success": True, "result": param.upper()}

# Add to TOOL_DEFINITIONS
{
    "name": "my_tool",
    "description": "What the tool does",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
}

# In src/mcp_server.py call_tool()
elif name == "my_tool":
    result = self.tools.my_tool(arguments.get("param", ""))
```

The client will automatically discover this new tool on next startup!

### Testing

```bash
# Test tools
python3 test_server.py

# Test in client
python3 main.py
```

---

## 📚 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Ollama Documentation](https://ollama.com/docs)
- [Ollama Model Library](https://ollama.com/library)

---

## 💡 Tips

1. Start with `llama3.2:3b` model for best balance
2. Use `reset` command to clear context and save memory
3. More detailed tool descriptions = better tool usage
4. Monitor resources with `htop` when running
5. Use tmux/screen for persistent sessions on cloud
6. The MCP server runs as a subprocess - you'll see "Starting MCP server subprocess" on startup
7. Tools are discovered dynamically - no need to restart client when adding tools to server

---

## 📄 License

This project is open source and available for use and modification.

---

## 🤝 Contributing

Feel free to:
- Submit issues
- Fork the repository
- Create pull requests
- Suggest new tools or features

---

**Built with ❤️ using Model Context Protocol and Ollama**

Questions? Open an issue on [GitHub](https://github.com/baliqbalpe/mcp-basic)

