# 🚀 Cloud Installation Instructions

## What You've Already Done

✅ Created virtual environment with `virtualenv venv`
✅ Activated virtual environment

## Next Steps

Since you already have the virtual environment activated `(venv)`, continue with these commands:

### 1. Install Dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Start Ollama Service

```bash
# Start Ollama in background
nohup ollama serve > ollama.log 2>&1 &

# Wait a few seconds for it to start
sleep 3
```

### 4. Pull the LLM Model

```bash
# This will download ~2GB, may take 5-15 minutes
ollama pull llama3.2:3b
```

### 5. Create Configuration File

```bash
cat > .env << 'EOF'
# MCP Configuration
MCP_SERVER_NAME=local-mcp-server
MCP_CLIENT_NAME=local-mcp-client

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000

# Logging
LOG_LEVEL=INFO
EOF
```

### 6. Create Data Directory

```bash
mkdir -p data
```

### 7. Test the Setup

```bash
python3 test_server.py
```

You should see output like:
```
==================================================
Testing MCP Server Tools
==================================================

1. Testing calculator...
   Result: {'success': True, 'result': 4, ...}
...
```

### 8. Start the MCP Client!

```bash
python3 main.py
```

## Using the Client

Once started, you'll see:

```
╭─────────────────────────────────────────╮
│ MCP Client with Local LLM               │
│ Using model: llama3.2:3b                │
╰─────────────────────────────────────────╯

You:
```

### Try These Commands:

1. **Ask for time**:
   ```
   You: What time is it?
   ```

2. **Do calculations**:
   ```
   You: Calculate 15 * 23 + 100
   ```

3. **List files**:
   ```
   You: List the files in the current directory
   ```

4. **System info**:
   ```
   You: What system am I running on?
   ```

### Special Commands:

- `exit` or `quit` - Exit the application
- `reset` - Clear conversation history
- `Ctrl+C` - Interrupt current operation

## Troubleshooting

### If Ollama isn't running:

```bash
# Check if running
pgrep -x ollama

# If not, start it
nohup ollama serve > ollama.log 2>&1 &
sleep 3
```

### If model isn't found:

```bash
# Check installed models
ollama list

# Pull the model again
ollama pull llama3.2:3b
```

### If imports fail:

```bash
# Make sure you're in the right directory
pwd
# Should show: /root/pdso-mcp

# Make sure venv is activated
which python3
# Should show: /root/pdso-mcp/venv/bin/python3
```

### If you need to reconnect later:

```bash
cd /root/pdso-mcp
source venv/bin/activate
python3 main.py
```

## Running in Background (Optional)

To keep it running after you disconnect:

```bash
# Install tmux
apt install -y tmux

# Start tmux session
tmux new -s mcp

# Run the client
python3 main.py

# Detach: Press Ctrl+B, then D
# Reattach later: tmux attach -t mcp
```

## Full Automated Setup (Alternative)

If you want to start fresh, you can now use the fixed setup script:

```bash
# Remove old venv
rm -rf venv

# Run setup script
./setup.sh
```

This will do everything automatically!

---

🎉 **That's it!** You now have a fully functional MCP client with local LLM running on your cloud machine.

