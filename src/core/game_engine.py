
from src.core.common import Millis
from src.core.states.game_state import GameState

class GameEngine:

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    
    def run_one_frame(self, time_passed: Millis):

        for npc in self.game_state.game_world.non_player_characters:
            npc.npc_mind.control_npc(self.game_state, npc, time_passed)
            npc.world_entity.update_movement_animation(time_passed)