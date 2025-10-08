# Deployment Guide for Cloud Machines

This guide will help you deploy the MCP Client & Server on various cloud platforms.

## 🌐 Supported Cloud Platforms

- DigitalOcean Droplets
- AWS EC2
- Google Cloud Compute Engine
- Azure Virtual Machines
- Linode
- Vultr
- Any Linux VPS

## 📦 Step-by-Step Deployment

### Step 1: Create a Cloud Machine

**Recommended Specifications:**
- OS: Ubuntu 22.04 LTS or later
- RAM: 4GB minimum (8GB recommended)
- CPU: 2 cores minimum (4 cores recommended)
- Storage: 20GB minimum
- Network: SSH access enabled

**For DigitalOcean:**
```bash
# Create a droplet with:
# - Ubuntu 22.04
# - 4GB RAM / 2 CPUs
# - SSH key authentication (as per your preference)
```

### Step 2: Connect to Your Cloud Machine

```bash
# SSH into your cloud machine
ssh root@your-cloud-ip

# Or with SSH key
ssh -i ~/.ssh/your-key root@your-cloud-ip
```

### Step 3: Update System

```bash
# Update package lists
apt update

# Upgrade installed packages
apt upgrade -y

# Install basic tools
apt install -y curl git build-essential
```

### Step 4: Install Python (if not already installed)

```bash
# Install Python 3 and pip
apt install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
```

### Step 5: Upload Project Files

**Option A: Using SCP**
```bash
# From your local machine
scp -r /path/to/mcp root@your-cloud-ip:/root/
```

**Option B: Using Git**
```bash
# On cloud machine
cd /root
git clone your-repository-url mcp
cd mcp
```

**Option C: Manual Upload**
```bash
# Create directory
mkdir -p /root/mcp

# Upload files using SFTP or your preferred method
```

### Step 6: Run Setup Script

```bash
# Navigate to project directory
cd /root/mcp

# Make scripts executable
chmod +x setup.sh start.sh

# Run setup
./setup.sh
```

The setup script will:
1. ✓ Create virtual environment
2. ✓ Install Python dependencies
3. ✓ Install Ollama
4. ✓ Start Ollama service
5. ✓ Pull the Llama 3.2 model
6. ✓ Create configuration files

**Note**: The initial model download may take 5-15 minutes depending on your connection speed.

### Step 7: Test the Installation

```bash
# Test the tools
source venv/bin/activate
python test_server.py
```

Expected output:
```
==================================================
Testing MCP Server Tools
==================================================

1. Testing calculator...
   Result: {'success': True, 'result': 4, 'expression': '2 + 2'}

2. Testing get_current_time...
   Result: {'success': True, 'datetime': '2025-10-08T...', ...}

...

All tests completed!
```

### Step 8: Start the MCP Client

```bash
# Using the start script
./start.sh

# Or manually
source venv/bin/activate
python main.py
```

## 🔄 Running in Background

To keep the client running after you disconnect:

### Option A: Using tmux (Recommended)

```bash
# Install tmux
apt install -y tmux

# Start a new tmux session
tmux new -s mcp

# Run the client
cd /root/mcp
./start.sh

# Detach from session: Press Ctrl+B, then D
# Reattach later: tmux attach -t mcp
```

### Option B: Using screen

```bash
# Install screen
apt install -y screen

# Start a new screen session
screen -S mcp

# Run the client
cd /root/mcp
./start.sh

# Detach: Press Ctrl+A, then D
# Reattach: screen -r mcp
```

### Option C: Using nohup

```bash
# Run in background
nohup ./start.sh > mcp.log 2>&1 &

# Check logs
tail -f mcp.log
```

## 🔧 Creating a Systemd Service (Advanced)

For production deployments, create a systemd service:

```bash
# Create service file
cat > /etc/systemd/system/mcp-client.service << 'EOF'
[Unit]
Description=MCP Client with Local LLM
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/mcp
Environment="PATH=/root/mcp/venv/bin"
ExecStart=/root/mcp/venv/bin/python /root/mcp/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
systemctl daemon-reload

# Enable and start service
systemctl enable mcp-client
systemctl start mcp-client

# Check status
systemctl status mcp-client

# View logs
journalctl -u mcp-client -f
```

## 🔐 Security Considerations

### 1. Firewall Configuration

```bash
# If using ufw (Ubuntu)
ufw allow ssh
ufw allow 11434/tcp  # Ollama (only if needed externally)
ufw enable
```

### 2. Create Non-Root User (Recommended)

```bash
# Create user
adduser mcpuser

# Add to sudo group
usermod -aG sudo mcpuser

# Switch to user
su - mcpuser

# Move project
sudo mv /root/mcp /home/mcpuser/
sudo chown -R mcpuser:mcpuser /home/mcpuser/mcp
```

### 3. Disable Root SSH (Optional)

```bash
# Edit SSH config
nano /etc/ssh/sshd_config

# Set: PermitRootLogin no

# Restart SSH
systemctl restart sshd
```

## 📊 Monitoring

### Check Ollama Status

```bash
# Check if Ollama is running
pgrep -x ollama

# Check Ollama logs
tail -f ~/mcp/ollama.log

# List installed models
ollama list
```

### Monitor System Resources

```bash
# Install htop
apt install -y htop

# Run htop
htop

# Or use top
top
```

### Check Disk Space

```bash
# Check disk usage
df -h

# Check directory size
du -sh /root/mcp
```

## 🔄 Updates and Maintenance

### Update the Project

```bash
cd /root/mcp
git pull  # If using git

# Or re-upload files
```

### Update Ollama

```bash
# Update Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Restart Ollama
pkill ollama
nohup ollama serve > ollama.log 2>&1 &
```

### Update Python Dependencies

```bash
cd /root/mcp
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Pull New Models

```bash
# Pull a new model
ollama pull mistral:latest

# Update .env file
nano .env
# Change: OLLAMA_MODEL=mistral:latest

# Restart client
```

## 🐛 Troubleshooting

### Issue: Ollama Not Starting

```bash
# Check logs
tail -f ~/mcp/ollama.log

# Kill and restart
pkill ollama
nohup ollama serve > ollama.log 2>&1 &
sleep 3
ollama pull llama3.2:3b
```

### Issue: Out of Memory

```bash
# Check memory usage
free -h

# Use a smaller model
ollama pull llama3.2:1b

# Update .env
nano .env
# Change: OLLAMA_MODEL=llama3.2:1b
```

### Issue: Model Download Failed

```bash
# Check internet connection
ping -c 3 ollama.com

# Try pulling again
ollama pull llama3.2:3b
```

### Issue: Python Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## 💰 Cost Optimization

### 1. Use Smaller Models
- `llama3.2:1b` - Smallest, fastest
- `llama3.2:3b` - Good balance

### 2. Stop When Not in Use
```bash
# Stop Ollama
pkill ollama

# Later, restart
nohup ollama serve > ollama.log 2>&1 &
```

### 3. Use Spot/Preemptible Instances
- AWS Spot Instances
- GCP Preemptible VMs
- Can save 50-90% on costs

## 📱 Accessing from Multiple Devices

### Option 1: SSH Tunnel

```bash
# From your local machine
ssh -L 11434:localhost:11434 root@your-cloud-ip

# Now you can connect to Ollama locally
```

### Option 2: Expose Ollama (Not Recommended for Production)

```bash
# Edit Ollama service to listen on all interfaces
# Only do this with proper firewall rules!
```

## ✅ Deployment Checklist

- [ ] Cloud machine created with adequate resources
- [ ] SSH access configured
- [ ] System updated (`apt update && apt upgrade`)
- [ ] Python 3.8+ installed
- [ ] Project files uploaded
- [ ] Setup script executed successfully
- [ ] Ollama service running
- [ ] Model downloaded
- [ ] Test script passed
- [ ] Client starts without errors
- [ ] Background execution configured (tmux/screen/systemd)
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup strategy in place

## 🎯 Quick Reference Commands

```bash
# Start client
cd /root/mcp && ./start.sh

# Stop Ollama
pkill ollama

# Start Ollama
nohup ollama serve > ollama.log 2>&1 &

# Check status
pgrep -x ollama && echo "Running" || echo "Not running"

# View logs
tail -f mcp.log

# Restart everything
pkill ollama
sleep 2
cd /root/mcp && ./start.sh
```

## 📞 Support

If you encounter issues:

1. Check logs: `tail -f ~/mcp/ollama.log`
2. Verify system resources: `htop` or `free -h`
3. Test tools: `python test_server.py`
4. Check Ollama: `ollama list`

---

Happy deploying! 🚀

