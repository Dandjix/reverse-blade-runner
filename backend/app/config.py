"""
Configuration centrale pour le backend du jeu Reverse Blade Runner.
Modifiez ici les constantes globales (nombre de bots, timeout, etc.).
"""


# Timeout (en secondes) pour une action (ex: réponse bot, accusation, etc.)
action_timeout = 15

# Longueur maximale d'un message
default_max_message_length = 300

# Liste des pseudos réservés (ex: noms système)
RESERVED_PSEUDOS = ["SYSTEM", "BOT", "ADMIN"]

# Statuts de partie
game_status = {
    "WAITING": "waiting",
    "RUNNING": "running",
    "ENDED": "ended"
}

# Valeurs par défaut supplémentaires
DEFAULT_ROOM_NAME = "room"
DEFAULT_MIN_PLAYERS = 2
DEFAULT_LANGUAGE = "french"
DEFAULT_BOT_COUNT = 3

# Ajoutez ici d'autres constantes ou paramètres globaux
