from app.core.room import Room
from typing import Dict

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def add_room(self, room_id: str, room: Room):
        self.rooms[room_id] = room

    def get_room(self, room_id: str) -> Room:
        return self.rooms.get(room_id)

room_manager = RoomManager()
