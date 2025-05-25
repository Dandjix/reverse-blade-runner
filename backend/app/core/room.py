from typing import Dict
from fastapi import WebSocket
from app.core.player import Player
from app.core.room_params import RoomParams
from app.core.room_manager import Bot
from app.services.llm_service import generate_bot_reply
import asyncio
import random

class Room:
    def __init__(self, name: str, language: str, min_players: int, nb_bots: int):
        self.params = RoomParams(name, language, min_players, nb_bots)
        self.human_players: Dict[str, Player] = {}
        self.human_sockets: Dict[str, WebSocket] = {}
        self.bots: Dict[str, Bot] = {}
        self.pseudos: Dict[str, str] = {}
        self.game_started: bool = False
        self.game_state = None
        self.message_history = []

    def add_human_player(self, player_id: str, websocket: WebSocket):
        self.human_players[player_id] = Player(player_id)
        self.human_sockets[player_id] = websocket

    def add_bot(self, bot: Bot):
        self.bots[bot.bot_id] = bot
        self.pseudos[bot.bot_id] = bot.pseudo

    async def broadcast(self, message: str):
        for ws in self.human_sockets.values():
            await ws.send_text(message)

    async def start_bot_responses(self):
        async def bot_loop():
            while self.game_started:
                if not self.bots:
                    await asyncio.sleep(1)
                    continue
                bot = random.choice(list(self.bots.values()))
                formatted_history = [f"{author}: {msg}" for author, msg in self.message_history]
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
                await asyncio.sleep(random.uniform(1, 5))
        asyncio.create_task(bot_loop())

    def get_all_players_info(self) -> list[dict]:
        players = []
        for player_id, player in self.human_players.items():
            pseudo = self.pseudos.get(player_id, "Inconnu")
            players.append({
                "id": player_id,
                "pseudo": pseudo,
                "is_human": True,
                "personality": None
            })
        for bot_id, bot in self.bots.items():
            players.append({
                "id": bot_id,
                "pseudo": bot.pseudo,
                "is_human": False,
                "personality": bot.personality
            })
        return players
