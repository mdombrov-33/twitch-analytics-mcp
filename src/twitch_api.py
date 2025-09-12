import os
from typing import List
from dotenv import load_dotenv
from twitchAPI.twitch import Twitch
from .database import StreamSnapshot
import traceback


class TwitchService:
    def __init__(self):
        load_dotenv()
        app_id = os.getenv("TWITCH_APP_ID")
        app_secret = os.getenv("TWITCH_APP_SECRET")

        if not app_id or not app_secret:
            raise ValueError(
                "Twitch API credentials are not set in environment variables."
            )

        self.app_id = app_id
        self.app_secret = app_secret

    async def get_trending_streams(self, limit: int = 20) -> List[StreamSnapshot]:
        """Fetch trending streams from Twitch API"""
        twitch = await Twitch(self.app_id, self.app_secret)
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
                if len(streams) >= limit:
                    break

            return streams
        finally:
            await twitch.close()


# Test function
async def test_twitch_api():
    """Simple test of the Twitch API connection"""
    print("Testing Twitch API connection...")
    service = TwitchService()
    try:
        streams = await service.get_trending_streams(5)
        print(f"Successfully fetched {len(streams)} trending streams:")
        for i, stream in enumerate(streams, 1):
            print(
                f"{i}. {stream.user_name}: {stream.viewer_count:,} viewers - {stream.game_name}"
            )
    except Exception as e:
        print(f"Error: {e}")

        traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_twitch_api())
