from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from manager import ConnectionManagerInstance
from ai_bot import get_ai_response
import asyncio

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    username = await ConnectionManagerInstance.connect(websocket)
    await ConnectionManagerInstance.broadcast(f"{username} joined the chat.")

    try:
        while True:
            message = await websocket.receive_text()
            await ConnectionManagerInstance.broadcast(f"{username}: {message}")

            if "@bot" in message.lower():
                asyncio.create_task(send_ai_reply(username, message))

    except WebSocketDisconnect:
        ConnectionManagerInstance.disconnect(websocket)
        await ConnectionManagerInstance.broadcast(f"{username} has disconnected.")

async def send_ai_reply(user: str, message: str):
    reply = await get_ai_response(message,user)
    await ConnectionManagerInstance.broadcast(f"bot 🤖: {reply}")
