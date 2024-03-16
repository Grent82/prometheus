from typing import List, Tuple

from pygame import Rect

from src.core.game_entity import WorldEntity
from src.core.states.game_world_state import GameWorldState

class GameState:
    def __init__(self, game_world_state: GameWorldState, camera_size: Tuple[int, int]):
        self.game_world = game_world_state
        self.camera_size = camera_size

    def get_all_entities_to_render(self) -> List[WorldEntity]:
        return self.game_world.get_renderable_entities()
    
    def get_walls_in_sight_of_player(self) -> List[WorldEntity]:
        return self.game_world.get_walls_in_sight_of_player(self.camera_world_area)
    
    def get_camera_world_area(self) -> Rect:
        camera_world_area = Rect(self.camera_world_area)
        return camera_world_area