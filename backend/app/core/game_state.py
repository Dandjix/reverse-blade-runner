from app.services.llm_service import generate_theme, generate_pseudos_and_personalities

class GameState:
    def __init__(self, language: str):
        self.theme = ""
        self.language = language
        self.players_data = []  # list of dicts {pseudo, personality}

    async def initialize(self, total_players: int):
        self.theme = await generate_theme(self.language)
        self.players_data = await generate_pseudos_and_personalities(self.theme, total_players, self.language)

