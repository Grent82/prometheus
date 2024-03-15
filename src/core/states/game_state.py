
from src.core.states.game_world_state import GameWorldState

class GameState:
    def __init__(self, game_world_state: GameWorldState):
        self.game_world_state = game_world_state