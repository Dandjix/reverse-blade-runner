import random
from app.llm.llm_service import generate_theme, generate_usernames

class GameState:
    def __init__(self, language: str):
        self.theme: str = ""
        self.language: str = language
        self.devineur: str = ""
        self.devine: str = ""
        self.pseudos: dict[str, str] = {}

    async def initialize(self, player_ids: list[str]):
        self.theme = await generate_theme(self.language)
        self.devineur, self.devine = random.sample(player_ids, 2)
        usernames = await generate_usernames(self.theme, len(player_ids), self.language)
        self.pseudos = dict(zip(player_ids, usernames))
