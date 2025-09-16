import apsw
from pathlib import Path
from datetime import datetime
from src.models import StreamSnapshot
from src.utils.logging_config import logger
from src.utils.exceptions import DatabaseError


class DatabaseService:
    """Handles all database operations for Twitch MCP"""

    def __init__(self, db_path: str = "twitch_mcp.db"):
        self.db_path = Path(db_path)
        self.connection = apsw.Connection(str(self.db_path))
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            self.connection.cursor().execute("PRAGMA foreign_keys = ON")
            self._create_tables()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise DatabaseError("Failed to initialize database")

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
            logger.info(f"Inserted {inserted_count} stream snapshots")
            return inserted_count
        except Exception as e:
            logger.error(f"Error inserting stream snapshots: {e}")
            raise DatabaseError(f"Failed to insert stream snapshots: {e}")

    def get_all_streams(self) -> list[StreamSnapshot]:
        """Fetch all stream snapshots from the database"""
        cursor = self.connection.cursor()
        query = """
            SELECT user_login, user_name, viewer_count, game_name, game_id,
                   title, timestamp, is_live, language
            FROM stream_snapshots
            ORDER BY timestamp DESC
        """
        try:
            rows = cursor.execute(query).fetchall()
            snapshots = []
            for row in rows:
                snapshot = StreamSnapshot(
                    user_login=str(row[0] or ""),
                    user_name=str(row[1] or ""),
                    viewer_count=int(row[2] or 0),
                    game_name=str(row[3]) if row[3] else None,
                    game_id=str(row[4]) if row[4] else None,
                    title=str(row[5] or ""),
                    timestamp=datetime.fromisoformat(str(row[6]))
                    if row[6]
                    else datetime.now(),
                    is_live=bool(row[7]) if row[7] is not None else False,
                    language=str(row[8] or "en"),
                )
                snapshots.append(snapshot)
            return snapshots
        except Exception as e:
            logger.error(f"Error fetching all streams: {e}")
            raise DatabaseError(f"Failed to fetch stream snapshots: {e}")
