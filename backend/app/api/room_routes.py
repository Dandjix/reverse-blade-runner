from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from app.core.room_manager import Room, room_manager

router = APIRouter()

class RoomConfig(BaseModel):
    name: str
    language: str
    min_players: int
    nb_bots: int

@router.post("/room/create")
def create_room(config: RoomConfig):
    room_id = "1234"
    # room_id = str(uuid.uuid4())
    room = Room(
        name=config.name,
        language=config.language,
        min_players=config.min_players,
        nb_bots=config.nb_bots
    )
    room_manager.add_room(room_id, room)
    return {
        "room_id": room_id,
        "params": {
            "name": config.name,
            "min_players": config.min_players,
            "language": config.language,
            "nb_bots": config.nb_bots
        }
    }



@router.get("/room/{room_id}")
def get_room_info(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}
    return {
        "room_id": room_id,
        "name": room.params.name,
        "language": room.params.language,
        "min_players": room.params.min_players,
        "nb_bots": room.params.nb_bots,
        "current_players": len(room.human_players),
        "game_started": room.game_started
    }

@router.get("/rooms")
def get_all_rooms():
    rooms = []
    for room_id, room in room_manager.rooms.items():
        rooms.append({
            "room_id": room_id,
            "name": room.params.name,
            "language": room.params.language,
            "min_players": room.params.min_players,
            "nb_bots": room.params.nb_bots,
            "current_players": len(room.human_players),
            "game_started": room.game_started
        })
    return {"rooms": rooms}


@router.get("/room/{room_id}/pseudos")
async def get_pseudos(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    pseudos = list(room.pseudos.values())
    return {"pseudos": pseudos}

@router.get("/room/{room_id}/players")
async def get_all_players(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    return {"players": room.get_all_players_info()}




