class Player:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.found_humans = set()  # pseudos des humains trouvés

    def add_found_human(self, pseudo: str):
        self.found_humans.add(pseudo)

    def has_found_all_humans(self, all_human_pseudos: set) -> bool:
        return all_human_pseudos <= self.found_humans
