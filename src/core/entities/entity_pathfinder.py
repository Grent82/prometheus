
from typing import List, Optional, Tuple

from pygame import Rect
from src.core.common import GRID_CELL_WIDTH, Direction, Millis, get_opposite_direction
from src.core.entities.game_entity import WorldEntity
from src.core.math import get_directions_to_position, is_x_and_y_within_distance
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.states.game_state import GameState

DEBUG_RENDER_PATHFINDING = False
DEBUG_PATHFINDER_INTERVAL = 900

class EntityPathfinder:
    def __init__(self, global_path_finder: GlobalPathFinder):
        self.path: List[Tuple[int, int]] = None  # This is expressed in game world coordinates (can be negative)
        self.global_path_finder: GlobalPathFinder = global_path_finder

    def update_path_towards_target(self, game_state: GameState, agent_entity: WorldEntity, target_entity: WorldEntity):
        agent_cell = _translate_world_position_to_cell(agent_entity.get_position(),
                                                       game_state.game_world.entire_world_area)
        target_cell = _translate_world_position_to_cell(target_entity.get_position(),
                                                        game_state.game_world.entire_world_area)

        agent_cell_size = (agent_entity.pygame_collision_rect.w // GRID_CELL_WIDTH + 1,
                           agent_entity.pygame_collision_rect.h // GRID_CELL_WIDTH + 1)
        self.global_path_finder.register_entity_size(agent_cell_size)
        path_with_cells = self.global_path_finder.run(agent_cell_size, agent_cell, target_cell)
        if path_with_cells:
            # Note: Cells are expressed in non-negative values (and need to be translated to game world coordinates)
            path = [_translate_cell_to_world_position(cell, game_state.game_world.entire_world_area) for cell in
                    path_with_cells]
            #if DEBUG_RENDER_PATHFINDING:
            #    _add_visual_lines_along_path(game_state, path)
            self.path = path
        else:
            self.path = None

    def get_next_waypoint_along_path(self, agent_entity: WorldEntity) -> Optional[Tuple[int, int]]:
        if self.path:
            # -----------------------------------------------
            # 1: Remove first waypoint if close enough to it
            # -----------------------------------------------
            closeness_margin = 50
            if is_x_and_y_within_distance(agent_entity.get_position(), self.path[0], closeness_margin):
                self.path.pop(0)
                if self.path:
                    return self.path[0]
                else:
                    return None

            # -----------------------------------------------
            # 2: Remove first waypoint if it's opposite direction of second waypoint
            # -----------------------------------------------
            if len(self.path) >= 2:
                dir_to_waypoint_0 = get_directions_to_position(agent_entity, self.path[0])[0]
                dir_to_waypoint_1 = get_directions_to_position(agent_entity, self.path[1])[0]
                if dir_to_waypoint_0 == get_opposite_direction(dir_to_waypoint_1):
                    self.path.pop(0)
                    return self.path[0]
                if self.path:
                    return self.path[0]
        else:
            return None
        return None

    @staticmethod
    def get_dir_towards_considering_collisions(game_state: GameState, agent_entity: WorldEntity,
                                               destination: Tuple[int, int]) -> Optional[Direction]:
        directions = get_directions_to_position(agent_entity, destination)
        if directions:
            if _would_collide_with_dir(directions[0], agent_entity, game_state):
                if len(directions) > 1 and directions[1]:
                    if not _would_collide_with_dir(directions[1], agent_entity, game_state):
                        return directions[1]
                    else:
                        return None
                else:
                    return None
            else:
                return directions[0]
        return None


def _would_collide_with_dir(direction: Direction, agent_entity: WorldEntity, game_state: GameState):
    future_time = Millis(100)
    future_pos = agent_entity.get_new_position_according_to_other_dir_and_speed(direction, future_time)
    future_pos_within_world = game_state.game_world.get_within_world(
        future_pos, (agent_entity.pygame_collision_rect.w, agent_entity.pygame_collision_rect.h))
    would_collide = game_state.game_world.would_entity_collide_if_new_pos(agent_entity, future_pos_within_world)
    return would_collide


def _translate_world_position_to_cell(position: Tuple[int, int], entire_world_area: Rect) -> Tuple[int, int]:
    return (int((position[0] - entire_world_area.x + GRID_CELL_WIDTH / 2) // GRID_CELL_WIDTH),
            int((position[1] - entire_world_area.y + GRID_CELL_WIDTH / 2) // GRID_CELL_WIDTH))


def _translate_cell_to_world_position(cell: Tuple[int, int], entire_world_area: Rect) -> Tuple[int, int]:
    return (cell[0] * GRID_CELL_WIDTH + entire_world_area.x,
            cell[1] * GRID_CELL_WIDTH + entire_world_area.y)