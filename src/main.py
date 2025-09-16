from fastmcp import FastMCP
from src.services.twitch_api import TwitchService
from src.db.database import DatabaseService
from src.utils.logging_config import logger
from src.decorators.mcp_exceptions import handle_mcp_exceptions
from src.utils.exceptions import DatabaseError

mcp = FastMCP("Twitch MCP")


@mcp.tool
@handle_mcp_exceptions
async def get_trending_channels(limit: int = 10) -> list[dict]:
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

        try:
            db_service.insert_stream_snapshots(streams)
        except Exception as db_error:
            raise DatabaseError(f"Failed to save stream snapshots: {db_error}")

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
            try:
                await twitch_service.close()
            except Exception as cleanup_error:
                logger.warning(f"Error during cleanup: {cleanup_error}")


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


@mcp.tool
@handle_mcp_exceptions
async def get_channel_current_performance(user_login: str) -> dict:
    """Get current performance metrics for a specific streamer

    Args:
        user_login: Twitch username of the streamer

    Returns:
        A dictionary with the streamer's current performance metrics
    """
    try:
        logger.info(f"Fetching current performance for user: {user_login}")

        twitch_service = TwitchService()
        db_service = DatabaseService("twitch_analytics.db")

        snapshot = await twitch_service.get_user_performance(user_login)

        try:
            db_service.insert_stream_snapshots([snapshot])
        except Exception as db_error:
            raise DatabaseError(f"Failed to save stream snapshot: {db_error}")

        result = {
            "user": snapshot.user_name,
            "viewers": snapshot.viewer_count,
            "game": snapshot.game_name,
            "title": snapshot.title,
            "language": snapshot.language,
            "is_live": snapshot.is_live,
            "timestamp": str(snapshot.timestamp),
        }

        logger.info(f"Successfully fetched performance for user: {user_login}")
        return result

    finally:
        if "twitch_service" in locals() and twitch_service:
            try:
                await twitch_service.close()
            except Exception as cleanup_error:
                logger.warning(f"Error during cleanup: {cleanup_error}")


@mcp.tool
@handle_mcp_exceptions
async def get_all_stream_snapshots_from_db() -> list[dict]:
    """Get all stored stream snapshots from the database

    Returns:
        List of all stream snapshots with their details
    """
    try:
        logger.info("Fetching all stored stream snapshots")

        db_service = DatabaseService("twitch_analytics.db")
        snapshots = db_service.get_all_streams()

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
            for s in snapshots
        ]

        logger.info(f"Successfully returned {len(result)} stored stream snapshots")
        return result

    except Exception as db_error:
        raise DatabaseError(f"Failed to fetch stored stream snapshots: {db_error}")


if __name__ == "__main__":
    mcp.run()
