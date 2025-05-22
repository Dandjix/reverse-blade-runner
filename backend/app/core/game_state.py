from app.llm.llm_service import generate_theme, generate_pseudos_and_personalities

class GameState:
    def __init__(self, language: str):
        self.theme: str = ""
        self.language: str = language
        self.pseudos: dict[str, str] = {}

    async def initialize(self, player_ids: list[str], nb_bots: int):
        self.theme = await generate_theme(self.language)

        all_count = len(player_ids) + nb_bots
        players_data = await generate_pseudos_and_personalities(self.theme, all_count, self.language)

        human_pseudos = players_data[:len(player_ids)]
        self.pseudos = dict(zip(player_ids, [p["pseudo"] for p in human_pseudos]))

        self.bots_data = [(p["pseudo"], p["personality"]) for p in players_data[len(player_ids):]]

