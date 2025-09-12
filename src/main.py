from fastmcp import FastMCP
from src.twitch_api import TwitchService
from src.database import DatabaseService

mcp = FastMCP("Twitch Analytics")


@mcp.tool
async def discover_trending_streamers(limit: int = 10) -> list[dict]:
    """Get current trending streamers from Twitch"""
    twitch_service = TwitchService()
    db_service = DatabaseService("twitch_analytics.db")

    streams = await twitch_service.get_trending_streams(limit)
    db_service.insert_stream_snapshots(streams)

    return [
        {
            "user": s.user_name,
            "viewers": s.viewer_count,
            "game": s.game_name,
            "title": s.title,
            "language": s.language,
            "is_live": s.is_live,
            "timestamp": str(s.timestamp),  # Convert datetime to string for JSON
        }
        for s in streams
    ]


@mcp.tool
async def get_top_games(limit: int = 10) -> list[dict]:
    """Get current top games from Twitch"""
    twitch_service = TwitchService()

    games = await twitch_service.get_top_games(limit)

    return [
        {
            "rank": g.rank,
            "game_name": g.game_name,
            "game_id": g.game_id,
            "box_art_url": g.box_art_url,
            "igdb_id": g.igdb_id,
            "timestamp": str(g.timestamp),  # Convert datetime to string for JSON
        }
        for g in games
    ]


if __name__ == "__main__":
    mcp.run()
