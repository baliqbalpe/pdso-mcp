# 🔧 Fix for Module Import Error

## The Problem

The MCP server couldn't find the `src` module when run as a subprocess because Python doesn't automatically include the parent directory in the path.

## Quick Fix on Your Cloud Machine

Run these commands on your cloud machine to fix the issue:

```bash
cd /root/pdso-mcp

# Pull the latest fixes from GitHub
git pull origin main

# Or if you haven't set up git yet, download the fixed files:
# We need to update src/mcp_server.py, src/config.py, and src/tools.py
```

## What Was Fixed

### 1. **src/mcp_server.py**
Added path handling at the beginning:

```python
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
```

### 2. **src/config.py**
Improved .env file loading:

```python
# Find and load .env from project root
current_dir = Path(__file__).parent
project_root = current_dir.parent
env_path = project_root / '.env'

load_dotenv(dotenv_path=env_path)
```

### 3. **src/tools.py**
Added sys import for consistency

## After Applying the Fix

```bash
# Test it
python3 main.py
```

You should now see:
```
Connecting to MCP server...
✓ Connected to MCP server

Available tools: calculator, get_current_time, list_files, ...

You:
```

## Alternative: Manual Fix

If you can't pull from GitHub, manually edit the files:

### Edit `/root/pdso-mcp/src/mcp_server.py`:

Add after the first docstring and before other imports:

```python
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
```

### Edit `/root/pdso-mcp/src/config.py`:

Replace the load_dotenv section:

```python
# Find and load .env from project root
current_dir = Path(__file__).parent
project_root = current_dir.parent
env_path = project_root / '.env'

# Load environment variables
load_dotenv(dotenv_path=env_path)
```

Then restart the client:

```bash
python3 main.py
```

## Why This Happened

When Python runs a script directly (like when MCP client spawns the server), it only includes:
1. The script's directory in sys.path
2. Standard library paths

It doesn't include the parent directory, so imports like `from src.tools import ...` fail.

Our fix explicitly adds the parent directory to Python's search path.

---

This fix is now in the GitHub repository. Pull it to get the latest working version! 🚀

