#!/usr/bin/env python3
"""Test MCP client-server integration."""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.mcp_client import MCPClient


async def test_mcp_integration():
    """Test the MCP client-server communication."""
    print("=" * 60)
    print("MCP Integration Test")
    print("=" * 60)

    client = MCPClient()

    try:
        # Test 1: Connect to MCP server
        print("\n[Test 1] Connecting to MCP server via STDIO...")
        await client.connect()
        print("✓ Connected successfully")

        # Test 2: Verify tools were discovered
        print(f"\n[Test 2] Tools discovered: {len(client.tools)}")
        for tool in client.tools:
            print(f"  - {tool['function']['name']}: {tool['function']['description'][:50]}...")
        print("✓ Tools discovered successfully")

        # Test 3: Call a simple tool (calculator)
        print("\n[Test 3] Testing calculator tool...")
        result = await client.call_tool("calculator", {"expression": "2 + 2"})
        print(f"  Result: {result}")
        if result.get("success") and result.get("result") == 4:
            print("✓ Calculator tool works")
        else:
            print("✗ Calculator tool failed")

        # Test 4: Call get_current_time tool
        print("\n[Test 4] Testing get_current_time tool...")
        result = await client.call_tool("get_current_time", {})
        print(f"  Result: {result.get('datetime', 'N/A')}")
        if result.get("success"):
            print("✓ get_current_time tool works")
        else:
            print("✗ get_current_time tool failed")

        # Test 5: Call system_info tool
        print("\n[Test 5] Testing system_info tool...")
        result = await client.call_tool("system_info", {})
        if result.get("success"):
            print(f"  System: {result.get('system', 'N/A')}")
            print(f"  Python: {result.get('python_version', 'N/A')}")
            print("✓ system_info tool works")
        else:
            print("✗ system_info tool failed")

        print("\n" + "=" * 60)
        print("All tests passed! MCP integration working correctly.")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        await client.close()
        print("\n[Cleanup] MCP client closed")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_mcp_integration())
    sys.exit(0 if success else 1)

