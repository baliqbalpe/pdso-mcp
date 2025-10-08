# Quick Command Reference

## Setup Commands (Run Once)

```bash
# Make scripts executable
chmod +x setup.sh start.sh

# Run automated setup (FIXED VERSION)
./setup.sh
```

## Manual Setup (Since You Already Started)

Since you already have `(venv)` activated:

```bash
# 1. Install dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Start Ollama
nohup ollama serve > ollama.log 2>&1 &
sleep 3

# 4. Download model
ollama pull llama3.2:3b

# 5. Create config
cp env.example .env

# 6. Create data directory
mkdir -p data

# 7. Test
python3 test_server.py

# 8. Run client
python3 main.py
```

## Daily Use Commands

```bash
# Start everything
./start.sh

# Or manually:
cd /root/pdso-mcp
source venv/bin/activate
python3 main.py
```

## Ollama Management

```bash
# Check if Ollama is running
pgrep -x ollama

# Start Ollama
nohup ollama serve > ollama.log 2>&1 &

# Stop Ollama
pkill ollama

# List installed models
ollama list

# Pull a model
ollama pull llama3.2:3b

# Check Ollama logs
tail -f ollama.log
```

## Testing

```bash
# Test server tools
python3 test_server.py

# Check Ollama is working
curl http://localhost:11434/api/tags
```

## CLI Commands (While Running)

- `exit` or `quit` - Exit application
- `reset` - Clear conversation history
- `Ctrl+C` - Interrupt

## Background Running

### Using tmux (Recommended):
```bash
# Install
apt install -y tmux

# Start session
tmux new -s mcp

# Run client
python3 main.py

# Detach: Ctrl+B then D
# Reattach: tmux attach -t mcp
# Kill session: tmux kill-session -t mcp
```

### Using screen:
```bash
# Install
apt install -y screen

# Start session
screen -S mcp

# Run client
python3 main.py

# Detach: Ctrl+A then D
# Reattach: screen -r mcp
```

## Troubleshooting

```bash
# Check Python version
python3 --version

# Check virtual environment
which python3
# Should show: /root/pdso-mcp/venv/bin/python3

# Reinstall dependencies
python3 -m pip install --force-reinstall -r requirements.txt

# Check system resources
free -h
df -h
top
```

## File Locations

```
/root/pdso-mcp/          # Project root
├── venv/                # Virtual environment
├── src/                 # Source code
├── data/                # Data directory
├── .env                 # Configuration
├── ollama.log           # Ollama logs
└── main.py              # Entry point
```

## Environment Variables (.env)

```bash
# Edit configuration
nano .env

# Available options:
# - OLLAMA_MODEL=llama3.2:3b
# - OLLAMA_HOST=http://localhost:11434
# - LOG_LEVEL=INFO
```

## Model Options

```bash
# Smallest (for low RAM)
ollama pull llama3.2:1b

# Recommended (4GB RAM)
ollama pull llama3.2:3b

# Better quality (8GB+ RAM)
ollama pull llama3:8b

# Alternative
ollama pull mistral:latest

# Then update .env:
# OLLAMA_MODEL=mistral:latest
```

## Logs and Monitoring

```bash
# Ollama logs
tail -f ollama.log

# MCP client logs (if running with nohup)
tail -f mcp.log

# System monitor
htop  # or just: top
```

## Clean Up

```bash
# Remove virtual environment
rm -rf venv

# Remove Ollama models
ollama rm llama3.2:3b

# Uninstall Ollama (if needed)
sudo systemctl stop ollama
sudo rm -rf /usr/local/bin/ollama
```

---

**Quick Start After Reboot:**

```bash
cd /root/pdso-mcp
source venv/bin/activate
nohup ollama serve > ollama.log 2>&1 &
sleep 3
python3 main.py
```

