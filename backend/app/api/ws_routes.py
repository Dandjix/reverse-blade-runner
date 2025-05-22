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

        if room.message_history:
            await websocket.send_text("💬 Previous messages:")
            for author, msg in room.message_history:
                await websocket.send_text(f"{author}: {msg}")

        while True:
            message = await websocket.receive_text()

            room.message_history.append((pseudo, message))
            await room.broadcast(f"{pseudo}: {message}")

    except WebSocketDisconnect:
        room.human_players.pop(player_id, None)
        room.pseudos.pop(player_id, None)
        await room.broadcast(f"🚪 {pseudo} disconnected.")