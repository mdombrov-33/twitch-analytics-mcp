from fastmcp import FastMCP
from src.services.twitch_api import TwitchService
from src.services.database import DatabaseService
from src.utils.logging_config import logger
from src.decorators.mcp_exceptions import handle_mcp_exceptions

mcp = FastMCP("Twitch Analytics")


@mcp.tool
@handle_mcp_exceptions
async def discover_trending_streamers(limit: int = 10) -> list[dict]:
    """Get current trending streamers from Twitch

    Args:
        limit: Maximum number of streamers to fetch (default: 10)

    Returns:
        List of trending streamers with their details
    """
    try:
        logger.info(f"Fetching {limit} trending streamers")

        twitch_service = TwitchService()
        db_service = DatabaseService("twitch_analytics.db")

        streams = await twitch_service.get_trending_streams(limit)
        db_service.insert_stream_snapshots(streams)

        result = [
            {
                "user": s.user_name,
                "viewers": s.viewer_count,
                "game": s.game_name,
                "title": s.title,
                "language": s.language,
                "is_live": s.is_live,
                "timestamp": str(s.timestamp),
            }
            for s in streams
        ]

        logger.info(f"Successfully returned {len(result)} trending streamers")
        return result

    finally:
        if "twitch_service" in locals() and twitch_service:
            await twitch_service.close()


@mcp.tool
@handle_mcp_exceptions
async def get_top_games(limit: int = 10) -> list[dict]:
    """Get current top games from Twitch

    Args:
        limit: Maximum number of games to fetch (default: 10)

    Returns:
        List of top games with their rankings and details
    """
    try:
        logger.info(f"Fetching {limit} top games")

        twitch_service = TwitchService()
        games = await twitch_service.get_top_games(limit)

        result = [
            {
                "rank": g.rank,
                "game_name": g.game_name,
                "game_id": g.game_id,
                "box_art_url": g.box_art_url,
                "igdb_id": g.igdb_id,
                "timestamp": str(g.timestamp),
            }
            for g in games
        ]

        logger.info(f"Successfully returned {len(result)} top games")
        return result

    finally:
        if "twitch_service" in locals() and twitch_service:
            try:
                await twitch_service.close()
            except Exception as cleanup_error:
                logger.warning(f"Error during cleanup: {cleanup_error}")


if __name__ == "__main__":
    mcp.run()
