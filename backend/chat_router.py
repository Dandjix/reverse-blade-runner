from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form
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

    except WebSocketDisconnect:
        ConnectionManagerInstance.disconnect(websocket)
        await ConnectionManagerInstance.broadcast(f"{username} has disconnected.")


@router.post("/context")
async def postContext(
        language: str = Form(...),
        context: str = Form(...),
        messageLengths: str = Form(...),
        messageFrequencySeconds: int = Form(...),
        nbBots: int = Form(...)
    ):
    """change le contexte et relance la partie."""
