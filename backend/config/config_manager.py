import json
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config(config_path=DEFAULT_CONFIG_PATH):
    """Charge la configuration depuis le fichier JSON spécifié"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data: dict, config_path=DEFAULT_CONFIG_PATH):
    """Écrit les nouvelles valeurs dans le fichier JSON spécifié"""
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_config_value(key: str, config_path=DEFAULT_CONFIG_PATH):
    """Récupère une valeur spécifique de config"""
    config = load_config(config_path)
    return config.get(key)

def set_config_value(key: str, value, config_path=DEFAULT_CONFIG_PATH):
    """Modifie une valeur spécifique et sauvegarde"""
    config = load_config(config_path)
    config[key] = value
    save_config(config, config_path)
    
def set_language(language: str, config_path=DEFAULT_CONFIG_PATH):
    set_config_value("language", language, config_path)

def get_language(config_path=DEFAULT_CONFIG_PATH):
    return get_config_value("language", config_path)

def set_nb_players(nb_players: int, config_path=DEFAULT_CONFIG_PATH):
    set_config_value("nbPlayers", nb_players, config_path)

def get_nb_players(config_path=DEFAULT_CONFIG_PATH):
    return get_config_value("nbPlayers", config_path)

def set_message_length(length: int, config_path=DEFAULT_CONFIG_PATH):
    set_config_value("messageLength", length, config_path)

def get_message_length(config_path=DEFAULT_CONFIG_PATH):
    return get_config_value("messageLength", config_path)

def set_message_frequency(frequency: int, config_path=DEFAULT_CONFIG_PATH):
    set_config_value("messageFrequency", frequency, config_path)

def get_message_frequency(config_path=DEFAULT_CONFIG_PATH):
    return get_config_value("messageFrequency", config_path)