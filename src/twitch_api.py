import os
from typing import List
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from .database import StreamSnapshot


class TwitchService:
    def __init__(self):
        load_dotenv()
        app_id = os.getenv("TWITCH_APP_ID")
        app_secret = os.getenv("TWITCH_APP_SECRET")
        self.twitch = None

        if not app_id or not app_secret:
            raise ValueError(
                "Twitch API credentials are not set in environment variables."
            )

        self.app_id = app_id
        self.app_secret = app_secret

    async def _get_client(self) -> Twitch:
        """Get or create Twitch API client"""
        if self.twitch is None:
            self.twitch = await Twitch(self.app_id, self.app_secret)
        return self.twitch

    async def close(self):
        """Clean up connection"""
        if self.twitch:
            await self.twitch.close()
            self.twitch = None

    async def get_trending_streams(self, limit: int = 10) -> List[StreamSnapshot]:
        """Fetch trending streams from Twitch API"""
        twitch = await self._get_client()

        try:
            streams = []
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

                # Stop when we reach the limit
                # If we don't write this then generator will fetch infinitely
                if len(streams) >= limit:
                    break

            return streams
        finally:
            await self.close()
