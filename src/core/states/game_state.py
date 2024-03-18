from typing import List, Tuple

from pygame import Rect

from src.core.common import GRID_CELL_WIDTH
from src.core.entities.game_entity import WorldEntity
from src.core.states.game_world_state import GameWorldState

class GameState:
    def __init__(self, game_world_state: GameWorldState, camera_size: Tuple[int, int]):
        self.game_world = game_world_state
        self.camera_size = camera_size
        self.camera_world_area = Rect((0, 0), self.camera_size)
        static_entities = [static_world_entity.world_entity for static_world_entity in game_world_state.static_entites.static_world_entities]
        self.pathfinder_grid = self._setup_pathfinder_grid(
            self.game_world.entire_world_area, static_entities)
        
    def _setup_pathfinder_grid(self, entire_world_area: Rect, static_entities: List[WorldEntity]):
        grid_width = entire_world_area.w // GRID_CELL_WIDTH
        grid_height = entire_world_area.h // GRID_CELL_WIDTH
        grid = []
        for x in range(grid_width + 1):
            grid.append((grid_height + 1) * [0])
        for static_entity in static_entities:
            cell_x = (static_entity.x - entire_world_area.x) // GRID_CELL_WIDTH
            cell_y = (static_entity.y - entire_world_area.y) // GRID_CELL_WIDTH
            grid[cell_x][cell_y] = 1
        return grid

    def get_all_entities_to_render(self) -> List[WorldEntity]:
        return self.game_world.get_renderable_entities()
    
    def get_walls_in_sight_of_player(self) -> List[WorldEntity]:
        return self.game_world.get_walls_in_sight_of_player(self.camera_world_area)
    
    def get_camera_world_area(self) -> Rect:
        camera_world_area = Rect(self.camera_world_area)
        return camera_world_area