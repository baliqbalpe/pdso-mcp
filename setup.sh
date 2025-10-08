#!/bin/bash

# MCP Client & Server Setup Script
# This script sets up the environment on a cloud machine

set -e

echo "========================================"
echo "MCP Client & Server Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3.8+ is installed
echo -e "\n${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${GREEN}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}Dependencies installed${NC}"

# Check if Ollama is installed
echo -e "\n${YELLOW}Checking for Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Ollama is not installed. Installing Ollama...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}Ollama installed${NC}"
else
    echo -e "${GREEN}Ollama is already installed${NC}"
fi

# Start Ollama service (if not running)
echo -e "\n${YELLOW}Starting Ollama service...${NC}"
if ! pgrep -x "ollama" > /dev/null; then
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
    echo -e "${GREEN}Ollama service started${NC}"
else
    echo -e "${GREEN}Ollama service is already running${NC}"
fi

# Pull the default model
echo -e "\n${YELLOW}Pulling Ollama model (llama3.2:3b)...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
ollama pull llama3.2:3b
echo -e "${GREEN}Model pulled successfully${NC}"

# Create data directory
echo -e "\n${YELLOW}Creating data directory...${NC}"
mkdir -p data
echo -e "${GREEN}Data directory created${NC}"

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "\n${YELLOW}Creating .env file...${NC}"
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
    echo -e "${GREEN}.env file created${NC}"
else
    echo -e "${GREEN}.env file already exists${NC}"
fi

echo -e "\n${GREEN}========================================"
echo -e "Setup completed successfully!"
echo -e "========================================${NC}"
echo -e "\n${YELLOW}To start the MCP client, run:${NC}"
echo -e "  source venv/bin/activate"
echo -e "  python main.py"
echo -e "\n${YELLOW}Or use the start script:${NC}"
echo -e "  ./start.sh"

