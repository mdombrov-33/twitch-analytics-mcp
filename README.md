# Twitch Analytics MCP Server

A Model Context Protocol (MCP) server that turns Claude Desktop into a Twitch analytics assistant. Analyze streamer performance, discover trending content, and get data-driven streaming insights using real Twitch API data.

## What is this?

This MCP server connects Claude Desktop to Twitch's API, giving you tools to:

- Analyze any streamer's performance and growth trends
- Find trending streamers and games in real-time
- Get optimal streaming time recommendations
- Compare streamers side-by-side
- Track game popularity over time

Instead of manually checking Twitch or using multiple analytics sites, just ask Claude questions like "How is pokimane performing this week?" or "What games are trending right now?"

## Tech Stack

- **FastMCP** - Server framework for Claude Desktop integration
- **twitchAPI** - Python wrapper for Twitch Helix API
- **APSW** - SQLite database (chosen for WSL2 compatibility)
- **APScheduler** - Background data collection
- **Pydantic** - Data validation and modeling

## How it works

```
Claude Desktop ←→ MCP Protocol ←→ FastMCP Server ←→ Twitch API
                                       ↓
                               SQLite Analytics Cache
```

The server runs in the background, collecting Twitch data every few minutes and caching it locally. When you ask Claude about Twitch analytics, it uses the MCP tools to query this data and give you instant insights.

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
4. Add server to Claude Desktop's MCP configuration via JSON file
5. Start asking Claude about Twitch data!

## Why MCP?

Model Context Protocol lets Claude Desktop integrate with external tools seamlessly. Instead of building a web interface or CLI, Claude becomes your natural language interface to Twitch analytics. Just talk to Claude like you're asking a Twitch expert.
