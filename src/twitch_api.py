import os
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from .models import StreamSnapshot, GameRanking
from .exceptions import ConfigurationError, ResourceNotFoundError
from .logging_config import logger
from .twitch_exceptions import handle_twitch_exceptions
from datetime import datetime


class TwitchService:
    def __init__(self):
        """Initialize TwitchService with API credentials"""
        try:
            load_dotenv()
            app_id = os.getenv("TWITCH_APP_ID")
            app_secret = os.getenv("TWITCH_APP_SECRET")
            self.twitch = None

            if not app_id or not app_secret:
                logger.error("Missing Twitch API credentials in environment variables")
                raise ConfigurationError(
                    "Twitch API credentials are not set. Please set TWITCH_APP_ID and TWITCH_APP_SECRET environment variables."
                )

            self.app_id = app_id
            self.app_secret = app_secret
            logger.info("TwitchService initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize TwitchService: {e}")
            raise

    async def _get_client(self):
        """Get or create Twitch API client"""
        if self.twitch is None:
            try:
                self.twitch = await Twitch(self.app_id, self.app_secret)
            except Exception as e:
                raise ConfigurationError(f"Failed to initialize Twitch API client: {e}")
        return self.twitch

    async def close(self):
        """Clean up connection"""
        if self.twitch:
            try:
                await self.twitch.close()
            except Exception as e:
                # Log warning but don't raise - cleanup should be non-critical
                logger.warning(f"Error while closing Twitch client: {e}")
            finally:
                self.twitch = None

    @handle_twitch_exceptions
    async def get_trending_streams(self, limit: int = 10) -> list[StreamSnapshot]:
        """Fetch trending streams from Twitch API

        Args:
            limit: Maximum number of streams to fetch

        Returns:
            List of stream snapshots

        Raises:
            AuthenticationError: Invalid or expired API credentials
            ServiceUnavailableError: Twitch API temporarily unavailable
            ResourceNotFoundError: No streams found
        """
        twitch = await self._get_client()
        streams: list[StreamSnapshot] = []

        async for stream in twitch.get_streams(first=limit):
            snapshot = StreamSnapshot(
                user_login=stream.user_login,
                user_name=stream.user_name,
                viewer_count=stream.viewer_count,
                game_name=stream.game_name,
                game_id=stream.game_id,
                title=stream.title,
                timestamp=stream.started_at,
                is_live=True,
                language=stream.language or "en",
            )
            streams.append(snapshot)

            if len(streams) >= limit:
                break

        if not streams:
            logger.warning("No trending streams found")
            raise ResourceNotFoundError("No trending streams are currently available")

        return streams

    @handle_twitch_exceptions
    async def get_top_games(self, limit: int = 10) -> list[GameRanking]:
        """Fetch top games from Twitch API

        Args:
            limit: Maximum number of games to fetch

        Returns:
            List of game rankings

        Raises:
            AuthenticationError: Invalid or expired API credentials
            ServiceUnavailableError: Twitch API temporarily unavailable
            ResourceNotFoundError: No games found
        """
        twitch = await self._get_client()
        games: list[GameRanking] = []

        async for game in twitch.get_top_games(first=limit):
            ranking = GameRanking(
                game_id=game.id,
                game_name=game.name,
                box_art_url=game.box_art_url,
                igdb_id=game.igdb_id,
                rank=len(games) + 1,
                timestamp=datetime.now(),
            )
            games.append(ranking)

            if len(games) >= limit:
                break

        if not games:
            logger.warning("No top games found")
            raise ResourceNotFoundError("No top games are currently available")

        return games
