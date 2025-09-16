import apsw
from pathlib import Path
from datetime import datetime
from src.models import StreamSnapshot


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
