# app/core/room_manager.py
from typing import Dict
from fastapi import WebSocket

class Bot:
    def __init__(self, bot_id: str, pseudo: str, personality: str):
        self.bot_id = bot_id
        self.pseudo = pseudo
        self.personality = personality

class RoomParams:
    def __init__(self, name, language, min_players, nb_bots):
        self.name = name
        self.language = language
        self.min_players = min_players
        self.nb_bots = nb_bots
        
class Room:
    def __init__(self, name: str, language: str, min_players: int, nb_bots: int):
        self.params = RoomParams(name, language, min_players, nb_bots)
        self.human_players = {}
        self.bots = {}
        self.pseudos = {}
        self.message_history = []
        self.guessed_by_player = {}
        self.game_started = False
        self.game_state = None

    def add_human_player(self, player_id: str, websocket: WebSocket):
        self.human_players[player_id] = websocket
        self.guessed_by_player[player_id] = set()

    def add_bot(self, bot: Bot):
        self.bots[bot.bot_id] = bot

    async def broadcast(self, message: str):
        """
        Send a message to all human players in the room.
        """
        for ws in self.human_players.values():
            await ws.send_text(message)

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def add_room(self, room_id: str, room: Room):
        self.rooms[room_id] = room

    def get_room(self, room_id: str) -> Room:
        return self.rooms.get(room_id)

room_manager = RoomManager()
