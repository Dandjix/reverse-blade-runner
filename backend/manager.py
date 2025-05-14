from collections import deque
from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.chat_history = deque(maxlen=100)  # Store the last 100 messages

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()
        username = None

        while not username or username in self.active_connections:
            username = await websocket.receive_text()

        self.active_connections[username] = websocket
        return username

    def disconnect(self, websocket: WebSocket):
        for name, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[name]
                break

    async def broadcast(self, message: str):
        self.chat_history.append(message)
        for conn in self.active_connections.values():
            await conn.send_text(message)

    async def send_to(self, username: str, message: str):
        if username in self.active_connections:
            await self.active_connections[username].send_text(message)
            
    def get_context(self) -> str:
        return "\n".join(self.chat_history)
    
ConnectionManagerInstance = ConnectionManager()