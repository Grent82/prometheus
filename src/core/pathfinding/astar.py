from abc import ABCMeta, abstractmethod
import heapq
from typing import List, Tuple

from src.core.common import Infinite

class Node:
    __slots__ = ('position', 'g_score', 'f_score', 'h_score'
                     'closed', 'came_from', 'out_openset')
    
    def __init__(self, position: Tuple[int, int], g_score:float = Infinite, f_score:float=Infinite):
        self.position = position
        self.came_from: Node = None
        self.g_score = g_score  # Cost from start node to current node
        self.h_score = .0       # Heuristic (estimated cost from current node to goal)
        self.f_score = f_score  # Total cost (g + h)
        self.out_openset = True
        self.closed = False

    def __lt__(self, other):
        return self.f_score < other.f_score

class AStar:
    __metaclass__ = ABCMeta
    __slots__ = ()
    
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    @abstractmethod
    def heuristic_cost_estimate(self, start: Tuple[int, int], goal: Tuple[int, int]):
        # Manhattan distance heuristic
        return abs(goal[0] - start[0]) + abs(goal[1] - start[1])

    @abstractmethod
    def neighbors(self, node: Tuple[int, int]) -> List[Node]:
        neighbors = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = node[0] + dr, node[1] + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != 1:
                neighbors.append(Node((r, c)))
        return neighbors
    
    @abstractmethod
    def distance_between(self, current: Tuple[int, int], goal: Tuple[int, int]):
        return 1
    
    def is_goal_reached(self, current: Tuple[int, int], goal: Tuple[int, int]):
        return current == goal

    def find_path(self, start: Node, goal: Node) -> List[Tuple[int, int]]:

        if self.is_goal_reached(start.position, goal.position):
            return [start]

        open_set = []

        start_node = Node(start)
        goal_node = Node(goal)

        start_node.g_score = start_node.h_score = start_node.f_score = 0

        heapq.heappush(open_set, start_node)

        while open_set:
            current_node = heapq.heappop(open_set)

            if self.is_goal_reached(current_node.position, goal_node.position):
                return self.reconstruct_path(current_node)
            
            current_node.closed = True
            current_node.out_openset = False

            for neighbor in self.neighbors(current_node):
                if neighbor.closed:
                    continue

                tentative_g_score = current_node.g_score + self.distance_between(current_node.position, neighbor.position)
                if tentative_g_score >= neighbor.g_score:
                    continue
                neighbor.came_from = current_node
                neighbor.g_score = tentative_g_score
                neighbor.h_score = self.heuristic_cost_estimate(neighbor.position, goal.position)
                neighbor.f_score = tentative_g_score + neighbor.h_score
                if neighbor.out_openset:
                    neighbor.out_openset = False
                    heapq.heappush(open_set, neighbor)

        return None  # No path found

    def reconstruct_path(self, current: Node) -> List[Tuple[int, int]]:
        path = []
        next_node = current
        while next_node is not None:
            path.append(next_node.position)
            next_node = next_node.came_from
        return path[::-1]
    
    