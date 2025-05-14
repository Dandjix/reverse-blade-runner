# filename: chat_app.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from random import randint

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        username = None
        
        while not username or username in self.active_connections :
            username = await websocket.receive_text()

        self.active_connections[username] = websocket
        return username

    def disconnect(self, websocket: WebSocket):
        key_rem = next((k for k, v in self.active_connections.items() if v == websocket), None)

        if key_rem:
            del self.active_connections[key_rem]

    async def broadcast(self, message: str):
        for key in self.active_connections:
            await self.active_connections[key].send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    username = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} has disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("chat_app:app", host="127.0.0.1", port=8000, reload=True)