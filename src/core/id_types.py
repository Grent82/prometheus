from typing import TypeVar, Dict

# Define a generic type for game IDs
GameIdT = TypeVar('GameIdT', bound=str)

# Define game ID types
GAME_ID_TYPES = {
    'worlds': 0,
    'agents': 0,
    'npcs' : 0,
    'conversations': 0
}

class GameId:
    _id_counters: Dict[str, int] = {}

    def __init__(self, game_id: GameIdT):
        if game_id not in self._id_counters:
            raise ValueError(f"Undefined game ID: {game_id}")
        self.game_id = game_id
        self.id = self._id_counters[game_id]
        self._id_counters[game_id] += 1
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, GameId):
            return self.game_id == other.game_id and self.id == other.id
        return NotImplemented

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        x = self.__eq__(other)
        if x is NotImplemented:
            return NotImplemented
        return not x



# Initialize ID counters
GameId._id_counters = GAME_ID_TYPES

def create_id(game_id: GameIdT) -> GameId:
    return GameId(game_id)
