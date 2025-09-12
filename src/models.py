from pydantic import BaseModel
from datetime import datetime


class StreamSnapshot(BaseModel):
    """Pydantic model for a stream snapshot data"""

    user_login: str
    user_name: str
    viewer_count: int
    game_name: str | None = None
    game_id: str | None = None
    title: str
    timestamp: datetime
    is_live: bool = True
    language: str = "en"


class UserAnalytics(BaseModel):
    """Pydantic model for user analytics data"""

    user_login: str
    user_name: str
    avg_viewers: int
    peak_viewers: int
    total_streams: int
    top_games: list[str]
    best_streaming_hours: list[str]
    last_updated: datetime


class GameTrend(BaseModel):
    """Pydantic model for game trend data"""

    game_id: str
    game_name: str
    total_viewers: int
    total_streams: int
    trend_score: float
    timestamp: datetime


class GameRanking(BaseModel):
    """Pydantic model for game ranking data"""

    game_id: str
    game_name: str
    box_art_url: str
    igdb_id: str | None = None
    rank: int
    timestamp: datetime
