from typing import Dict
from fastapi import WebSocket
import asyncio
import random
from app.services.llm_service import generate_bot_reply

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
        self.human_players: Dict[str, WebSocket] = {}
        self.bots: Dict[str, Bot] = {}
        self.pseudos: Dict[str, str] = {}
        self.game_started: bool = False
        self.game_state = None
        self.message_history = []

    def add_human_player(self, player_id: str, websocket: WebSocket):
        self.human_players[player_id] = websocket

    def add_bot(self, bot: Bot):
        self.bots[bot.bot_id] = bot

    async def broadcast(self, message: str):
        """
        Send a message to all players in the room.
        """
        for ws in self.human_players.values():
            await ws.send_text(message)
            
    async def start_bot_responses(self):
        async def bot_loop():
            while self.game_started:
                if not self.bots:
                    await asyncio.sleep(1)
                    continue

                # Choix aléatoire d’un bot
                bot = random.choice(list(self.bots.values()))

                # Récupère l'historique formaté
                formatted_history = [f"{author}: {msg}" for author, msg in self.message_history]

                # Génère une réponse via LLM
                try:
                    message = await generate_bot_reply(
                        pseudo=bot.pseudo,
                        personality=bot.personality,
                        theme=self.game_state.theme,
                        language=self.params.language,
                        history=formatted_history
                    )
                except Exception as e:
                    print(f"Bot LLM error: {e}")
                    await asyncio.sleep(1)
                    continue

                self.message_history.append((bot.pseudo, message))
                await self.broadcast(f"{bot.pseudo}: {message}")

                await asyncio.sleep(random.uniform(1, 5))  # Pause aléatoire entre les messages

        asyncio.create_task(bot_loop())
        
    def get_all_players_info(self) -> list[dict]:
        players = []

        # Ajoute les humains
        for player_id, websocket in self.human_players.items():
            pseudo = self.pseudos.get(player_id, "Inconnu")
            players.append({
                "id": player_id,
                "pseudo": pseudo,
                "is_human": True,
                "personality": None
            })

        # Ajoute les bots
        for bot_id, bot in self.bots.items():
            players.append({
                "id": bot_id,
                "pseudo": bot.pseudo,
                "is_human": False,
                "personality": bot.personality
            })

        return players

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def add_room(self, room_id: str, room: Room):
        self.rooms[room_id] = room

    def get_room(self, room_id: str) -> Room:
        return self.rooms.get(room_id)

room_manager = RoomManager()
