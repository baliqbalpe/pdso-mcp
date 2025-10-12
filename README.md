# MCP Client with Local LLM

A complete Model Context Protocol (MCP) client with local LLM integration using Ollama. Chat with AI that can use tools - no API keys needed, runs entirely on your machine.

**Repository**: https://github.com/baliqbalpe/pdso-mcp

---

## 🚀 Quick Start

Get up and running in 3 steps:

```bash
# 1. Clone the repository
git clone https://github.com/baliqbalpe/pdso-mcp.git
cd pdso-mcp

# 2. Run automated setup
chmod +x setup.sh start.sh
./setup.sh

# 3. Start chatting!
./start.sh
```

That's it! The setup script installs everything automatically.

---

## 🌟 Features

- ✅ **Local LLM** - Runs Ollama models (Llama 3.2, Mistral) locally
- ✅ **7 Built-in Tools** - File operations, calculations, system info
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

## 💻 Installation

### Automated Installation (Recommended)

```bash
git clone https://github.com/baliqbalpe/pdso-mcp.git
cd pdso-mcp
chmod +x setup.sh
./setup.sh
```

### Manual Installation

```bash
# 1. Create virtual environment
python3 -m virtualenv venv
source venv/bin/activate

# 2. Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 3. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 4. Start Ollama and pull model
nohup ollama serve > ollama.log 2>&1 &
sleep 3
ollama pull llama3.2:3b

# 5. Create config
cp env.example .env
mkdir -p data
```

### Cloud Deployment

Perfect for DigitalOcean, AWS, GCP, Azure, etc.:

```bash
# SSH into your cloud machine
ssh root@your-cloud-ip

# Clone and setup
git clone https://github.com/baliqbalpe/pdso-mcp.git
cd pdso-mcp
./setup.sh

# Run in background with tmux
apt install -y tmux
tmux new -s mcp
./start.sh

# Detach: Ctrl+B then D
# Reattach: tmux attach -t mcp
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
cd /root/pdso-mcp
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
pwd  # Should show: /root/pdso-mcp

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
cd /root/pdso-mcp
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
pdso-mcp/
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── tools.py           # MCP tools
│   ├── mcp_client.py      # Client with Ollama
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
2. Add tool definition to `TOOL_DEFINITIONS`
3. Add routing in `src/mcp_client.py` `call_tool()` method

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

# In src/mcp_client.py call_tool()
elif tool_name == "my_tool":
    result = self.mcp_tools.my_tool(arguments.get("param", ""))
```

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

Questions? Open an issue on [GitHub](https://github.com/baliqbalpe/pdso-mcp)

