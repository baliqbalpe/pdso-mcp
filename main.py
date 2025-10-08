#!/usr/bin/env python3
"""Main entry point for MCP client CLI."""

import sys
from src.cli import main
import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

