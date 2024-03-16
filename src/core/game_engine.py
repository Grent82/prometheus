
from src.core.common import Millis
from src.core.states.game_state import GameState

class GameEngine:

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    
    def run_one_frame(self, time_passed: Millis):

        for npc in self.game_state.game_world.entities:
            pass   