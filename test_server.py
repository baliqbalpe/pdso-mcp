#!/usr/bin/env python3
"""Test script to verify MCP server tools work correctly."""

import asyncio
from src.tools import MCPTools

async def test_tools():
    """Test all MCP server tools."""
    tools = MCPTools()

    print("=" * 50)
    print("Testing MCP Server Tools")
    print("=" * 50)

    # Test calculator
    print("\n1. Testing calculator...")
    result = tools.calculator("2 + 2")
    print(f"   Result: {result}")

    # Test get_current_time
    print("\n2. Testing get_current_time...")
    result = tools.get_current_time()
    print(f"   Result: {result}")

    # Test list_files
    print("\n3. Testing list_files...")
    result = tools.list_files(".")
    print(f"   Found {result.get('count', 0)} items")

    # Test system_info
    print("\n4. Testing system_info...")
    result = tools.system_info()
    print(f"   System: {result.get('system', 'unknown')}")

    # Test write_file
    print("\n5. Testing write_file...")
    result = tools.write_file("data/test.txt", "Hello, MCP!")
    print(f"   Result: {result}")

    # Test read_file
    print("\n6. Testing read_file...")
    result = tools.read_file("data/test.txt")
    print(f"   Content: {result.get('content', '')}")

    # Test execute_command
    print("\n7. Testing execute_command...")
    result = tools.execute_command("echo 'Hello from command'")
    print(f"   Output: {result.get('stdout', '').strip()}")

    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_tools())

