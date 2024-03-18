
from typing import Any, Dict, List, Optional, Tuple

from src.core.pathfinding.astar import AStar, Node

path_finder = None

def init_global_path_finder():
    global path_finder
    path_finder = GlobalPathFinder()
    return path_finder


def get_global_path_finder():
    return path_finder


class GridBasedAStar(AStar):
    def __init__(self, grid, agent_size: Tuple[int, int]):
        self.grid = grid
        self.agent_size = agent_size
        self._cache_is_cell_free: Dict[Tuple[int, int], bool] = {}

        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def set_pathfinding_bounds(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def neighbors(self, node: Tuple[int, int]):
        x, y = node
        adjacent_cells = [
            (x, y - 1),  # up
            (x - 1, y),  # left
            (x + 1, y),  # right
            (x, y + 1),  # down
        ]
        return [cell for cell in adjacent_cells if self._is_cell_free(cell[0], cell[1])]
    
    def _is_cell_free(self, x, y):
        # Ignore cells that are too far out, to save resources. If agent strays too far, the path is aborted.
        if not (self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y):
            return False

        if (x, y) in self._cache_is_cell_free:
            return self._cache_is_cell_free[(x, y)]
        else:
            is_free = self._compute_is_cell_free(x, y)
            self._cache_is_cell_free[(x, y)] = is_free
            return is_free
        
    def _compute_is_cell_free(self, x, y):
        # Check that all relevant cells are within the map
        if x < 0 or y < 0 or x + self.agent_size[0] >= len(self.grid) or y + self.agent_size[1] >= len(self.grid[x]):
            return False
        for _x in range(x, x + self.agent_size[0]):
            for _y in range(y, y + self.agent_size[1]):
                if self.grid[_x][_y] == 1: # blocked
                    return False
        return True

class GlobalPathFinder:
    def __init__(self):
        self.grid = None
        self.astars_by_entity_size: Dict[Tuple[int, int], GridBasedAStar] = {}
        self.path_max_distance_from_start = 20

    def set_grid(self, grid):
        self.grid = grid

    def register_entity_size(self, size: Tuple[int, int]):
        if not size in self.astars_by_entity_size:
            self.astars_by_entity_size[size] = GridBasedAStar(self.grid, size)

    def set_max_distance_from_start(self, distance=20):
        self.path_max_distance_from_start = distance

    def run(self, entity_size: Tuple[int, int], start_cell: Tuple[int, int], goal_cell: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:

        astar = self.astars_by_entity_size[entity_size]
        astar.set_pathfinding_bounds(start_cell[0] - self.path_max_distance_from_start,
                                     start_cell[1] - self.path_max_distance_from_start,
                                     start_cell[0] + self.path_max_distance_from_start,
                                     start_cell[1] + self.path_max_distance_from_start)
        start_node = Node(start_cell)
        goal_node = Node(goal_cell)
        path = astar.find_path(start_node, goal_node)

        if path is None:
            for alternative_goal in astar.neighbors(goal_cell):
                alternative_goal_node = Node(alternative_goal)
                path = astar.find_path(start_node, alternative_goal_node)
                if path:
                    break
        
        if path is None:
            return None

        path_list = []
        for x in path:
            path_list.append(x)

        return path_list
    
    def _get_alternative_goals(self, goal_cell: Tuple[int, int]):
        alternative_goals = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = goal_cell[0] + dr, goal_cell[1] + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != 1:
                alternative_goals.append((r, c))
        return alternative_goals
    
