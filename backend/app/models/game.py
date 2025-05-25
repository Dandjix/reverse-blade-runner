from pydantic import BaseModel
from typing import Optional
from app.config import DEFAULT_BOT_COUNT, DEFAULT_ROOM_NAME, DEFAULT_MIN_PLAYERS, DEFAULT_LANGUAGE

class RoomParams(BaseModel):
    name: str = DEFAULT_ROOM_NAME
    min_players: int = DEFAULT_MIN_PLAYERS
    nb_bots: int = DEFAULT_BOT_COUNT
    language: Optional[str] = DEFAULT_LANGUAGE
