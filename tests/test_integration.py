import asyncio
import sys
from pathlib import Path
from src.services.twitch_api import TwitchService
from src.services.database import DatabaseService

# Add the parent directory to sys.path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))


async def test_api_to_database_pipeline():
    """Test the complete pipeline: Twitch API -> Database -> Retrieval"""
    print("Starting integration test...")

    # Initialize services
    print("\nInitializing services...")
    twitch_service = TwitchService()
    db_service = DatabaseService("test_integration.db")

    try:
        # Fetch data from Twitch API
        print("Fetching streams from Twitch API...")
        api_streams = await twitch_service.get_trending_streams(3)
        print(f"Fetched {len(api_streams)} streams from API")

        for i, stream in enumerate(api_streams, 1):
            print(f"  {i}. {stream.user_name}: {stream.viewer_count:,} viewers")

        # Save to database
        print("\nSaving streams to database...")
        inserted_count = db_service.insert_stream_snapshots(api_streams)
        print(f"Saved {inserted_count} streams to database")

        # Retrieve from database
        print("\nRetrieving streams from database...")
        db_streams = db_service.get_recent_streams(5)
        print(f"Retrieved {len(db_streams)} streams from database")

        for i, stream in enumerate(db_streams, 1):
            print(f"  {i}. {stream.user_name}: {stream.viewer_count:,} viewers")

        # Verify data integrity
        print("\nVerifying data integrity...")

        if len(api_streams) == len(db_streams):
            print(f"Count matches: {len(api_streams)} streams")
        else:
            print(f"Count mismatch: API={len(api_streams)}, DB={len(db_streams)}")
            return False

        api_usernames = {s.user_name for s in api_streams}
        db_usernames = {s.user_name for s in db_streams}

        if api_usernames == db_usernames:
            print(f"Usernames match: {api_usernames}")
        else:
            print("Username mismatch:")
            print(f"  API: {api_usernames}")
            print(f"  DB:  {db_usernames}")
            return False

        # Check data structure
        sample_db_stream = db_streams[0]
        print("Sample data structure:")
        print(
            f"  user_name: {type(sample_db_stream.user_name).__name__} = '{sample_db_stream.user_name}'"
        )
        print(
            f"  viewer_count: {type(sample_db_stream.viewer_count).__name__} = {sample_db_stream.viewer_count}"
        )
        print(
            f"  timestamp: {type(sample_db_stream.timestamp).__name__} = {sample_db_stream.timestamp}"
        )
        print(
            f"  is_live: {type(sample_db_stream.is_live).__name__} = {sample_db_stream.is_live}"
        )

        print("\nIntegration test PASSED! Pipeline is working correctly.")
        return True

    except Exception as e:
        print(f"\nIntegration test FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_api_to_database_pipeline())
    exit(0 if success else 1)
