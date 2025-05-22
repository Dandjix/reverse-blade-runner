# app/api/room_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
import uuid
from app.core.room_manager import Room, room_manager, Bot
from app.core.game_state import GameState

router = APIRouter()

class RoomConfig(BaseModel):
    name: str
    language: str
    min_players: int
    nb_bots: int

@router.post("/room/create")
def create_room(config: RoomConfig):
    room_id = str(uuid.uuid4())
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


@router.post("/room/{room_id}/start")
async def start_game(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    if room.game_started:
        return {"message": "Game already started"}

    if len(room.human_players) < room.params.min_players:
        return {"error": "Not enough players"}

    player_ids = list(room.human_players.keys())
    room.game_state = GameState(room.params.language)
    await room.game_state.initialize(player_ids, room.params.nb_bots)

    room.pseudos.update(room.game_state.pseudos)
    
    for i, (pseudo, personality) in enumerate(room.game_state.bots_data):
        bot_id = str(uuid.uuid4())[:8]
        bot = Bot(bot_id, pseudo, personality)
        room.add_bot(bot)
        room.pseudos[bot_id] = pseudo
        # room.message_history.append((pseudo, f"*{pseudo}, {personality}, has joined the chat.*"))


    room.game_started = True
    await room.broadcast(f"🎮 Game started! Theme: {room.game_state.theme}") # broadcast to send to everyone
    for pid, ws in room.human_players.items():
        await ws.send_text(f"Your pseudo: {room.pseudos[pid]}") # send_text to send to each player privately

    return {"status": "started"}

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


@router.get("/room/{room_id}/players")
async def get_players(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    pseudos = list(room.pseudos.values())
    return {"pseudos": pseudos}


@router.post("/room/{room_id}/blame/{pseudo}")
async def blame_player(room_id: str, pseudo: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    player_id = next((pid for pid, p in room.pseudos.items() if p == pseudo), None)
    if not player_id:
        return {"error": "Pseudo not found"}

    is_human = player_id in room.human_players

    return {
        "pseudo": pseudo,
        "was_human": is_human
    }

