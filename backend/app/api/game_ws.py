# app/ws/game_ws.py
import uuid
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.room_manager import room_manager

router = APIRouter()

@router.websocket("/ws/room/{room_id}")
async def websocket_room_endpoint(websocket: WebSocket, room_id: str):
    room = room_manager.get_room(room_id)
    if not room:
        await websocket.close(code=1000)
        return

    await websocket.accept()
    player_id = str(uuid.uuid4())[:8]
    room.add_human_player(player_id, websocket)

    await websocket.send_text(f"✔️ Connected to room {room_id} with id {player_id}")

    try:
        while not room.game_started:
            # await websocket.send_text("⏳ Waiting for the game to start...")
            await asyncio.sleep(1)

        theme = room.game_state.theme if room.game_state else "(unknown)"
        pseudo = room.pseudos.get(player_id, f"Player{player_id[:4]}")
        room.pseudos[player_id] = pseudo

        await websocket.send_text(f"🎮 Game started! Theme: {theme}")
        await websocket.send_text(f"Your pseudo: {pseudo}")

        if room.message_history:
            await websocket.send_text("💬 Previous messages:")
            for author, msg in room.message_history:
                await websocket.send_text(f"{author}: {msg}")

        while True:
            message = await websocket.receive_text()

            if message.startswith("guess:"):
                await handle_guess(room, player_id, message[6:].strip())
            else:
                room.message_history.append((pseudo, message))
                await room.broadcast(f"{pseudo}: {message}")

    except WebSocketDisconnect:
        room.human_players.pop(player_id, None)
        room.guessed_by_player.pop(player_id, None)
        room.pseudos.pop(player_id, None)
        await room.broadcast(f"🚪 {pseudo} disconnected.")


async def handle_guess(room, player_id: str, guess_pseudo: str):
    guessed_id = next((pid for pid, p in room.pseudos.items() if p == guess_pseudo), None)
    player_ws = room.human_players.get(player_id)

    if guessed_id is None:
        await player_ws.send_text(f"❌ Unknown pseudo '{guess_pseudo}'")
        return

    if guessed_id == player_id:
        await player_ws.send_text("❌ You cannot guess yourself.")
        return

    if guessed_id in room.human_players:
        room.guessed_by_player[player_id].add(guessed_id)
        await room.broadcast(f"✔️ {room.pseudos[player_id]} guessed {guess_pseudo}!")

        if len(room.guessed_by_player[player_id]) == len(room.human_players) - 1:
            room.game_started = False
            await room.broadcast(f"🏆 {room.pseudos[player_id]} has won the game!")
    else:
        await player_ws.send_text(f"❌ {guess_pseudo} is not a human player. Try again.")
