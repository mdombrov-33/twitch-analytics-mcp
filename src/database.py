import apsw
from pathlib import Path
from datetime import datetime
from .models import StreamSnapshot


class DatabaseService:
    """Handles all database operations for Twitch MCP"""

    def __init__(self, db_path: str = "twitch_mcp.db"):
        self.db_path = Path(db_path)
        self.connection = apsw.Connection(str(self.db_path))
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            # Enable foreign keys
            self.connection.cursor().execute("PRAGMA foreign_keys = ON")
            self._create_tables()
            self._create_indexes()
            print(f"Database initialized at {self.db_path}")
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def _create_tables(self):
        """Create all required tables"""
        cursor = self.connection.cursor()

        # Stream snapshots table - stores real-time stream data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stream_snapshots(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_login TEXT NOT NULL,
                user_name TEXT NOT NULL,
                viewer_count INTEGER NOT NULL,
                game_name TEXT,
                game_id TEXT,
                title TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                is_live BOOLEAN NOT NULL DEFAULT 1,
                language TEXT DEFAULT 'en'
            )
        """)

        # User analytics summary data - aggregated stream stats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_analytics(
                user_login TEXT PRIMARY KEY,
                user_name TEXT NOT NULL,
                avg_viewers INTEGER DEFAULT 0,
                peak_viewers INTEGER DEFAULT 0,
                total_streams INTEGER DEFAULT 0,
                top_games TEXT, -- JSON array
                best_streaming_hours TEXT, -- JSON array
                last_updated DATETIME NOT NULL
            )
        """)

        # Game trends table - tracks game popularity
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_trends(
                game_id TEXT PRIMARY KEY,
                game_name TEXT NOT NULL,
                total_viewers INTEGER DEFAULT 0,
                total_streams INTEGER DEFAULT 0,
                trend_score REAL DEFAULT 0.0,
                timestamp DATETIME NOT NULL
            )
        """)

    def _create_indexes(self):
        """Create indexes for optimal query performance"""
        cursor = self.connection.cursor()

        #! STREAM_SNAPSHOTS INDEXES

        # Most common query: Get recent streams by user
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_user_timestamp 
            ON stream_snapshots(user_login, timestamp DESC)
        """)

        # Query streams by game over time
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_game_timestamp 
            ON stream_snapshots(game_id, timestamp DESC)
        """)

        # Query by timestamp for time-based analytics
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_timestamp 
            ON stream_snapshots(timestamp DESC)
        """)

        # Query live streams
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_live 
            ON stream_snapshots(is_live, timestamp DESC)
        """)

        # Composite index for viewer count analytics by user
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_snapshots_user_viewers 
            ON stream_snapshots(user_login, viewer_count DESC)
        """)

        #! USER_ANALYTICS INDEXES

        # Query top streamers by average viewers
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analytics_avg_viewers 
            ON user_analytics(avg_viewers DESC)
        """)

        # Query top streamers by peak viewers
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analytics_peak_viewers 
            ON user_analytics(peak_viewers DESC)
        """)

        # Query by last updated for cache invalidation
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_analytics_last_updated 
            ON user_analytics(last_updated)
        """)

        #! GAME_TRENDS INDEXES

        # Query trending games
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trends_score_timestamp 
            ON game_trends(trend_score DESC, timestamp DESC)
        """)

        # Query games by total viewers
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trends_total_viewers 
            ON game_trends(total_viewers DESC)
        """)

    def insert_stream_snapshots(self, snapshots: list[StreamSnapshot]) -> int:
        """Insert multiple stream snapshots into the database"""
        if not snapshots:
            return 0

        cursor = self.connection.cursor()

        # Prepare the insert query
        query = """
            INSERT INTO stream_snapshots 
            (user_login, user_name, viewer_count, game_name, game_id, 
             title, timestamp, is_live, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Convert snapshots to tuples for bulk insert
        data = []
        for snapshot in snapshots:
            data.append(
                (
                    snapshot.user_login,
                    snapshot.user_name,
                    snapshot.viewer_count,
                    snapshot.game_name,
                    snapshot.game_id,
                    snapshot.title,
                    snapshot.timestamp.isoformat() if snapshot.timestamp else None,
                    1 if snapshot.is_live else 0,
                    snapshot.language,
                )
            )

        try:
            cursor.executemany(query, data)
            inserted_count = len(data)
            print(f"Inserted {inserted_count} stream snapshots")
            return inserted_count
        except Exception as e:
            print(f"Error inserting stream snapshots: {e}")
            raise

    def get_recent_streams(self, limit: int = 20) -> list[StreamSnapshot]:
        """Get recent stream snapshots from database"""
        cursor = self.connection.cursor()

        query = """
            SELECT user_login, user_name, viewer_count, game_name, game_id,
                   title, timestamp, is_live, language
            FROM stream_snapshots 
            ORDER BY timestamp DESC 
            LIMIT ?
        """

        try:
            rows = cursor.execute(query, (limit,)).fetchall()
            snapshots = []

            for row in rows:
                # Convert SQLite values to proper Python types
                timestamp_str = str(row[6]) if row[6] else None
                timestamp = (
                    datetime.fromisoformat(timestamp_str)
                    if timestamp_str
                    else datetime.now()
                )

                snapshot = StreamSnapshot(
                    user_login=str(row[0]),
                    user_name=str(row[1]),
                    viewer_count=int(row[2]) if row[2] is not None else 0,
                    game_name=str(row[3]) if row[3] else None,
                    game_id=str(row[4]) if row[4] else None,
                    title=str(row[5]),
                    timestamp=timestamp,
                    is_live=bool(row[7]),
                    language=str(row[8]),
                )
                snapshots.append(snapshot)

            return snapshots
        except Exception as e:
            print(f"Error fetching recent streams: {e}")
            raise
