#!/usr/bin/env python3
"""Quick script to check database contents"""

import sys
from pathlib import Path
from src.database import DatabaseService

# Add the parent directory to sys.path so we can import from src
sys.path.append(str(Path(__file__).parent.parent))


def main():
    db = DatabaseService("test_integration.db")

    print("Database Contents:")
    print("-" * 40)

    streams = db.get_recent_streams(limit=100)

    if not streams:
        print("No streams found in database")
        return

    print(f"Found {len(streams)} stream snapshots:\n")

    for i, stream in enumerate(streams, 1):
        print(f"{i}. {stream.user_name}")
        print(f"   Viewers: {stream.viewer_count:,}")
        print(f"   Game: {stream.game_name}")
        print(f"   Title: {stream.title[:60]}...")
        print(f"   Time: {stream.timestamp}")
        print(f"   Live: {stream.is_live}")
        print()


if __name__ == "__main__":
    main()
