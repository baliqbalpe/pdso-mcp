# 🚀 Quick Start Guide

Get up and running with MCP Client & Server in 5 minutes!

## For Cloud Machines

### 1️⃣ Upload Project to Cloud

```bash
# SSH into your cloud machine
ssh root@your-cloud-ip

# Create directory
mkdir -p /root/mcp
cd /root/mcp

# Upload files via SCP from your local machine:
# scp -r /path/to/mcp/* root@your-cloud-ip:/root/mcp/
```

### 2️⃣ Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

Wait for:
- ✓ Dependencies installation
- ✓ Ollama installation
- ✓ Model download (llama3.2:3b ~2GB)

### 3️⃣ Start the Client

```bash
./start.sh
```

### 4️⃣ Start Chatting!

```
You: What time is it?
