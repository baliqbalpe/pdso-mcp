#!/bin/bash

# Start script for MCP Client

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Please run ./setup.sh first${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
. venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}Starting Ollama service...${NC}"
    nohup ollama serve > ollama.log 2>&1 &
    sleep 3
    echo -e "${GREEN}Ollama service started${NC}"
fi

# Start the MCP client
echo -e "${GREEN}Starting MCP Client...${NC}\n"
python3 main.py

