[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-blue?style=for-the-badge)](https://github.com/jlowin/fastmcp)
[![Twitch](https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white)](https://twitch.tv)
[![MCP Server](https://img.shields.io/badge/MCP-Server-brightgreen?style=for-the-badge&logo=claude&logoColor=white)](https://modelcontextprotocol.io)

# Twitch MCP Server

A comprehensive Model Context Protocol (MCP) server that provides full Twitch integration through any MCP-compatible client. Control your stream, manage your community, analyze performance, and automate Twitch operations using natural language commands and real Twitch API data.

## What is this?

This MCP server connects any MCP client to Twitch's API, giving you tools to:

- **Query Twitch Data** - Get top games, streamers, and performance metrics
- **Access Historical Data** - Retrieve cached information for analysis
- **Stream Control** - Manage your Twitch channel operations
- **Community Management** - Handle moderation and interactive features

Instead of using multiple tools and dashboards, just ask your MCP client natural language questions like "What are the top games right now?" or "How is shroud performing today?"



## Tech Stack

- **FastMCP** - MCP server framework
- **twitchAPI** - Python wrapper for Twitch Helix API
- **APSW** - SQLite database (cross-platform compatibility)
- **Pydantic** - Data validation and modeling

## How it works

```
MCP Client ←→ MCP Protocol ←→ FastMCP Server ←→ Twitch API
                                    ↓
                            SQLite Cache & History
```

When you ask questions or make requests, the server fetches real-time data from Twitch's API and can also query cached historical data. This enables both current information and trend analysis through natural language queries.

## MCP Client Compatibility

Works with any MCP-compatible client including:

- Claude Desktop
- Tome (supports multiple AI models like Qwen, GPT-4, etc.)
- Custom MCP implementations
- Third-party MCP clients
- Your own applications using MCP libraries

## Current Features

- Get top games on Twitch
- Get top channels/streamers
- Get performance data by user login
- Retrieve data from local database

The server provides both live Twitch API data and cached historical data, enabling natural language queries about Twitch content and performance. More Twitch API integrations coming soon.

## Setup

1. Get Twitch API credentials from [dev.twitch.tv](https://dev.twitch.tv/)
   - You'll need appropriate OAuth scopes for the features you want to use
2. Install dependencies: `poetry install`
3. Configure environment variables in `.env`
4. Add server to your MCP client's configuration
5. Start controlling Twitch through natural language commands!

## Configuration Examples

### Claude Desktop Configuration

Add the following to your Claude Desktop `claude_desktop_config.json` file:

**For WSL:**

```json
{
  "mcpServers": {
    "twitch-server": {
      "command": "wsl",
      "args": [
        "bash",
        "-c",
        "cd /path/to/your/twitch-mcp && poetry run python -m src.main"
      ],
      "env": {
        "TWITCH_APP_ID": "your_app_id_here",
        "TWITCH_APP_SECRET": "your_app_secret_here"
      }
    }
  }
}
```

**For Windows:**

```json
{
  "mcpServers": {
    "twitch-server": {
      "command": "powershell",
      "args": [
        "-Command",
        "cd 'C:\\path\\to\\your\\twitch-mcp'; poetry run python -m src.main"
      ],
      "env": {
        "TWITCH_APP_ID": "your_app_id_here",
        "TWITCH_APP_SECRET": "your_app_secret_here"
      }
    }
  }
}
```

**For Linux/macOS:**

```json
{
  "mcpServers": {
    "twitch-server": {
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/your/twitch-mcp && poetry run python -m src.main"
      ],
      "env": {
        "TWITCH_APP_ID": "your_app_id_here",
        "TWITCH_APP_SECRET": "your_app_secret_here"
      }
    }
  }
}
```

**Important Notes:**

- Replace `/path/to/your/twitch-mcp` with the actual path to your project directory
- Replace `your_app_id_here` and `your_app_secret_here` with your actual Twitch API credentials
- Ensure Poetry is installed and available in your system PATH
- Different features require different OAuth scopes - check Twitch API documentation
- For WSL, make sure the path uses Linux-style forward slashes
- For Windows, use backslashes in the path and escape them in JSON
