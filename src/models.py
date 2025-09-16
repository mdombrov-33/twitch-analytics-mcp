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


class GameRanking(BaseModel):
    """Pydantic model for game ranking data"""

    game_id: str
    game_name: str
    box_art_url: str
    igdb_id: str | None = None
    rank: int
    timestamp: datetime
