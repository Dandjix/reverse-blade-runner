from pydantic import BaseModel
from typing import Optional

class RoomParams(BaseModel):
    name: str
    min_players: int
    nb_bots: int
    language: Optional[str] = "english"
