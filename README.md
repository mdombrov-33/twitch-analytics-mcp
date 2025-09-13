[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-blue?style=for-the-badge)](https://github.com/jlowin/fastmcp)
[![Twitch](https://img.shields.io/badge/Twitch-9146FF?style=for-the-badge&logo=twitch&logoColor=white)](https://twitch.tv)
[![MCP Server](https://img.shields.io/badge/MCP-Server-brightgreen?style=for-the-badge&logo=claude&logoColor=white)](https://modelcontextprotocol.io)

# Twitch Analytics MCP Server

A Model Context Protocol (MCP) server that provides comprehensive Twitch analytics through any MCP-compatible client. Analyze streamer performance, discover trending content, and get data-driven streaming insights using real Twitch API data.

## What is this?

This MCP server connects any MCP client to Twitch's API, giving you tools to:

- Analyze any streamer's performance and growth trends
- Find trending streamers and games in real-time
- Get optimal streaming time recommendations
- Compare streamers side-by-side
- Track game popularity over time

Instead of manually checking Twitch or using multiple analytics sites, just ask your MCP client questions like "How is pokimane performing this week?" or "What games are trending right now?"

<p align="center">
  <img src="twitch-analytics.gif" alt="Demo Gif" width="1200"/>
</p>

## Tech Stack

- **FastMCP** - MCP server framework
- **twitchAPI** - Python wrapper for Twitch Helix API
- **APSW** - SQLite database (cross-platform compatibility)
- **Pydantic** - Data validation and modeling

## How it works

```
MCP Client ←→ MCP Protocol ←→ FastMCP Server ←→ Twitch API
                                    ↓
                            SQLite Analytics History
```

When you ask questions about Twitch analytics, the server makes fresh API calls to fetch real-time data and optionally caches it to build historical analytics. Every tool call gets the latest live data directly from Twitch.

## MCP Client Compatibility

Works with any MCP-compatible client including:

- Claude Desktop
- Tome (supports multiple AI models like Qwen, GPT-4, etc.)
- Custom MCP implementations
- Third-party MCP clients
- Your own applications using MCP libraries

## Features (Planned)

**Phase 1 - Core Analytics**

- `discover_trending_streamers` - Find top live streamers
- `analyze_game_trends` - Current game popularity
- `analyze_streamer_performance` - Viewer stats and growth

**Phase 2 - Advanced Features**

- `optimal_streaming_times` - Best hours/days to stream
- `compare_streamers` - Side-by-side comparisons
- `analyze_my_follows` - Your following list analysis

And 9 more tools for comprehensive Twitch analytics.

## Setup

1. Get Twitch API credentials from [dev.twitch.tv](https://dev.twitch.tv/)
2. Install dependencies: `poetry install`
3. Configure environment variables in `.env`
4. Add server to your MCP client's configuration
5. Start querying Twitch data through your preferred MCP client!

## Configuration Examples

### Claude Desktop Configuration

Add the following to your Claude Desktop `claude_desktop_config.json` file:

**For WSL:**

```json
{
  "mcpServers": {
    "twitch-analytics": {
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
    "twitch-analytics": {
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
    "twitch-analytics": {
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
- For WSL, make sure the path uses Linux-style forward slashes
- For Windows, use backslashes in the path and escape them in JSON

## Why MCP?

Model Context Protocol provides a standardized way for AI systems and applications to access external tools and data sources. Instead of building custom integrations for each client, this server works with any MCP-compatible system, making Twitch analytics accessible through natural language queries across different platforms.
