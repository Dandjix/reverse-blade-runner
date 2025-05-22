from fastapi import APIRouter
from app.core.room_manager import room_manager, Bot
from app.core.game_state import GameState
import asyncio
import uuid

router = APIRouter()

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
    
@router.post("/room/{room_id}/start")
async def start_game(room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        return {"error": "Room not found"}

    if room.game_started:
        return {"message": "Game already started"}

    if len(room.human_players) < room.params.min_players:
        return {"error": "Not enough players"}

    await room.broadcast("🔄 Game is starting...")
    player_ids = list(room.human_players.keys())
    total_players = len(player_ids) + room.params.nb_bots

    room.game_state = GameState(room.params.language)
    await room.game_state.initialize(total_players)

    # Pseudos pour les humains, pas besoin de personnalité
    human_players_data = room.game_state.players_data[:len(player_ids)]
    room.pseudos.update({pid: data["pseudo"] for pid, data in zip(player_ids, human_players_data)})

    # Bots avec pseudo + personnalité
    bots_data = room.game_state.players_data[len(player_ids):]
    for i, bot_info in enumerate(bots_data):
        bot_id = str(uuid.uuid4())[:8]
        bot = Bot(bot_id, bot_info["pseudo"], bot_info["personality"])
        room.add_bot(bot)
        room.pseudos[bot_id] = bot_info["pseudo"]

    room.game_started = True
    asyncio.create_task(room.start_bot_responses())

    await room.broadcast(f"🎮 Game started! Theme: {room.game_state.theme}") # broadcast to send to everyone
    for pid, ws in room.human_players.items():
        if pid in room.pseudos:
            await ws.send_text(f"Your pseudo: {room.pseudos[pid]}") # send_text to send to each player privately

    return {"status": "started"}
