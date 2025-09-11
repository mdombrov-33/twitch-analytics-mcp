---
applyTo: "**"
---

# Twitch Analytics MCP Server - Development Guidelines

## Project Overview

This project builds an MCP (Model Context Protocol) server that transforms Claude Desktop into a Twitch analytics assistant. The server provides real-time streamer performance analysis, game trend discovery, and optimal streaming time suggestions using the Twitch Helix API.

## Architecture & Tech Stack

- **FastMCP** - MCP server framework for Claude Desktop integration
- **python-twitch-api** - Python wrapper for Twitch Helix API
- **APSW** - SQLite database wrapper (chosen for WSL2/Windows compatibility)
- **APScheduler** - Background data collection scheduling
- **python-dotenv** - Environment variable management

## Key Resources

- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **Twitch API Python Library**: https://github.com/Teekeks/pyTwitchAPI
- **Twitch Helix API Docs**: https://dev.twitch.tv/docs/api/

## Development Approach

### Code Organization

- **Class-based approach preferred** - Use classes for services and tool groupings
- **Separation of concerns** - Keep API logic, database operations, and MCP tools separate
- **Modular structure** - Tools organized by functionality (streamer tools vs game tools)

### Implementation Guidelines

1. **Never modify files directly** - Always provide code snippets for manual implementation
2. **Ask before assuming** - If library-specific implementation details are unclear, request documentation
3. **Exact implementation may vary** - Focus on concepts and structure over rigid code copying
4. **Test incrementally** - Implement and test features step by step

### Library-Specific Notes

- **Twitch API**: Rate limiting is critical (800 requests/minute), implement proper token management
- **FastMCP**: Use unique tool names to avoid conflicts with other MCP servers
- **APSW**: Chosen over sqlite3 for better WSL2/Claude Desktop compatibility
- **Background tasks**: Use APScheduler for periodic data collection

### Project Structure

```
twitch-mcp/
├── .env                              # Environment variables (API keys)
├── .gitignore                        # Git ignore patterns
├── pyproject.toml                    # Poetry configuration
├── .github/
│   └── instructions/
│       └── instructions.md           # This file
└── src/
    └── twitch_analytics_mcp/
        ├── __init__.py               # Package initialization
        ├── main.py                   # MCP server entry point & scheduler
        ├── twitch_api.py             # Twitch API client & rate limiting
        ├── database.py               # Database schema & operations
        └── tools/
            ├── __init__.py           # Tools package init
            ├── streamer_tools.py     # Streamer analysis MCP tools
            └── game_tools.py         # Game trend analysis MCP tools
```

## MCP Tools Implementation Plan

### All 15 Planned Tools

**Phase 1 - Easy Testing (Start Here)**
1. `discover_trending_streamers` - Get top live streamers (no auth needed, immediate results)
2. `analyze_game_trends` - Current top games on Twitch (public data, visual results)
3. `analyze_streamer_performance` - Basic streamer stats (testable with any popular streamer)

**Phase 2 - Core Analytics**
4. `optimal_streaming_times` - Best streaming hours analysis (needs historical data)
5. `compare_streamers` - Side-by-side streamer comparison (2-5 streamers)
6. `weekly_activity_report` - Weekly streamer activity summary
7. `game_popularity_tracker` - Track game viewership trends over time

**Phase 3 - Advanced Features**  
8. `analyze_my_follows` - Personal following list analysis (requires user auth)
9. `live_alert_suggestions` - Suggest live streams to watch
10. `favorite_games_watchlist` - Aggregate streams from favorite games
11. `underrated_streamers` - Find low-viewer, high-growth streamers
12. `game_to_streamer_recommendation` - Suggest streamers by game preference

**Phase 4 - Complex Analytics**
13. `engagement_score_calculator` - Estimate engagement from viewer/chat ratios
14. `top_clips` - Most viewed clips (if API supports)
15. `historical_viewership_chart` - Long-term viewership data visualization

### Testing Strategy for Non-Streamers

- **Phase 1 tools** are perfect for testing - they use public data and give immediate results
- Test with popular streamers like: ninja, pokimane, xqc, shroud (always have data)
- Use popular games: Valorant, League of Legends, Just Chatting, Fortnite
- Start with recent time periods (last 7 days) to ensure data availability

### Commit Standards

- Use scope-feature-commit format for one-liner commits
- Commit after each logical development step
- Keep commits focused and atomic

### Environment Considerations

- **WSL2 compatibility** - Database and file operations must work across WSL2/Windows boundary
- **Claude Desktop integration** - MCP server runs as background process, not web service
- **No web framework needed** - Direct MCP protocol communication, no HTTP endpoints

## Development Workflow

1. Implement database schema and connection handling
2. Set up Twitch API client with proper authentication
3. Create Phase 1 MCP tools (easiest testing)
4. Add background data collection
5. Test integration with Claude Desktop
6. Implement remaining phases incrementally

Remember: If unsure about specific library usage or API details, request documentation rather than making assumptions.

# Twitch Analytics MCP Server - Development Guidelines

## Project Overview

This project builds an MCP (Model Context Protocol) server that transforms Claude Desktop into a Twitch analytics assistant. The server provides real-time streamer performance analysis, game trend discovery, and optimal streaming time suggestions using the Twitch Helix API.

## Architecture & Tech Stack

- **FastMCP** - MCP server framework for Claude Desktop integration
- **twitchAPI** - Python wrapper for Twitch Helix API
- **APSW** - SQLite database wrapper (chosen for WSL2/Windows compatibility)
- **APScheduler** - Background data collection scheduling
- **python-dotenv** - Environment variable management

## Development Approach

### Code Organization

- **Class-based approach preferred** - Use classes for services and tool groupings
- **Separation of concerns** - Keep API logic, database operations, and MCP tools separate
- **Modular structure** - Tools organized by functionality (streamer tools vs game tools)

### Implementation Guidelines

1. **Never modify files directly** - Always provide code snippets for manual implementation
2. **Ask before assuming** - If library-specific implementation details are unclear, request documentation
3. **Exact implementation may vary** - Focus on concepts and structure over rigid code copying
4. **Test incrementally** - Implement and test features step by step

### Library-Specific Notes

- **Twitch API**: Rate limiting is critical (800 requests/minute), implement proper token management
- **FastMCP**: Use unique tool names to avoid conflicts with other MCP servers
- **APSW**: Chosen over sqlite3 for better WSL2/Claude Desktop compatibility
- **Background tasks**: Use APScheduler for periodic data collection

### Project Structure

src/twitch_analytics_mcp/ ├── main.py # MCP server entry point ├── twitch_api.py # Twitch API client and rate limiting ├── database.py # Database schema and operations └── tools/ ├── streamer_tools.py # Streamer analysis MCP tools └── game_tools.py # Game trend analysis MCP tools

### Commit Standards

- Use scope-feature-commit format for one-liner commits
- Commit after each logical development step
- Keep commits focused and atomic

### Environment Considerations

- **WSL2 compatibility** - Database and file operations must work across WSL2/Windows boundary
- **Claude Desktop integration** - MCP server runs as background process, not web service
- **No web framework needed** - Direct MCP protocol communication, no HTTP endpoints

## MCP Tools to Implement

Core analytics tools for Claude integration:

- Streamer performance analysis
- Optimal streaming time recommendations
- Trending streamer discovery
- Game trend analysis
- Personal following analysis
- Cross-streamer comparisons

## Development Workflow

1. Implement database schema and connection handling
2. Set up Twitch API client with proper authentication
3. Create core MCP tools with error handling
4. Add background data collection
5. Test integration with Claude Desktop
6. Iterate and refine based on testing

Remember: If unsure about specific library usage or API details, request documentation rather than making assumptions.
