#!/usr/bin/env python3
"""CLI interface for MCP client."""

import asyncio
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp_client import MCPClient
from src.config import OLLAMA_MODEL

console = Console()


class MCPChatCLI:
    """Interactive CLI for MCP client."""

    def __init__(self):
        self.client = MCPClient()
        self.running = False

    async def start(self):
        """
        Start the CLI interface.
        """
        self.running = True

        # Display welcome message
        console.print(Panel.fit(
            "[bold cyan]MCP Client with Local LLM[/bold cyan]\n"
            f"Using model: [yellow]{OLLAMA_MODEL}[/yellow]\n"
            "Type your messages and press Enter. Type 'exit' or 'quit' to stop.\n"
            "Type 'reset' to clear conversation history.",
            border_style="cyan"
        ))

        # Initialize MCP client
        try:
            console.print("\n[yellow]Starting MCP server subprocess...[/yellow]")
            console.print("[yellow]Connecting to MCP server via STDIO...[/yellow]")
            await self.client.connect()
            console.print("[green]✓ MCP server connected[/green]")
            console.print("[green]✓ MCP session initialized[/green]\n")

            # Display available tools (discovered via MCP protocol)
            tools_list = [tool['function']['name'] for tool in self.client.tools]
            console.print(f"[cyan]Discovered {len(tools_list)} tools via MCP protocol:[/cyan]")
            console.print(f"[dim]{', '.join(tools_list)}[/dim]\n")

        except Exception as e:
            console.print(f"[red]✗ Failed to initialize MCP client: {e}[/red]")
            return

        # Main chat loop
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]You[/bold green]")

                if not user_input.strip():
                    continue

                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("\n[yellow]Goodbye![/yellow]")
                    break

                if user_input.lower() == 'reset':
                    self.client.reset_conversation()
                    console.print("[yellow]Conversation history cleared[/yellow]")
                    continue

                # Show thinking indicator
                console.print("\n[dim]Thinking...[/dim]")

                # Get response from LLM
                response = await self.client.chat(user_input)

                # Display response
                console.print("\n[bold cyan]Assistant:[/bold cyan]")
                console.print(Markdown(response))

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")

        # Cleanup
        await self.client.close()


async def main():
    """Main entry point for CLI."""
    # Start CLI
    cli = MCPChatCLI()
    await cli.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
        sys.exit(0)

