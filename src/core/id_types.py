from typing import TypeVar, Dict

# Define a generic type for game IDs
GameIdT = TypeVar('GameIdT', bound=str)

# Define game ID types
GAME_ID_TYPES = {
    'Worlds': 0,
    'Agents': 0,
    'Npc' : 0
}

class GameId:
    _id_counters: Dict[str, int] = {}

    def __init__(self, game_id: GameIdT):
        if game_id not in self._id_counters:
            raise ValueError(f"Undefined game ID: {game_id}")
        self.game_id = game_id
        self.id = self._id_counters[game_id]
        self._id_counters[game_id] += 1



# Initialize ID counters
GameId._id_counters = GAME_ID_TYPES

def create_id(game_id: GameIdT) -> GameId:
    return GameId(game_id)
