from pydantic import BaseModel, Field

class RoomCreateRequest(BaseModel):
    room_name: str = Field(..., min_length=1)
    max_users: int = Field(..., ge=1, le=100)

class RoomResponse(BaseModel):
    room_id: str
    room_name: str
    max_users: int
