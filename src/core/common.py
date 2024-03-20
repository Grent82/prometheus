
from enum import Enum
from typing import NewType, Any, List, Callable

Millis = NewType('Millis', int)
Infinite = float('inf')

GRID_CELL_WIDTH = 25

class Sprite(Enum):
    NONE = 0
    NPC = 1

class NpcType(Enum):
    MALE =  0
    FEMALE =  1
    MALE_CHILD =  2
    FEMALE_CHILD = 3

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class StaticWorldEntityType(Enum):
    WALL = 10
    WALL_DIRECTIONAL_N = 11
    WALL_DIRECTIONAL_NE = 12
    WALL_DIRECTIONAL_E = 13
    WALL_DIRECTIONAL_SE = 14
    WALL_DIRECTIONAL_S = 15
    WALL_DIRECTIONAL_SW = 16
    WALL_DIRECTIONAL_W = 17
    WALL_DIRECTIONAL_NW = 18
    WALL_DIRECTIONAL_POINTY_NE = 20
    WALL_DIRECTIONAL_POINTY_SE = 21
    WALL_DIRECTIONAL_POINTY_SW = 22
    WALL_DIRECTIONAL_POINTY_NW = 23
    CHAIR_RIGHT = 30
    CHAIR_DOWN = 31
    CHAIR_LEFT = 32
    CHAIR_UP = 33
    BED = 40

class Observable:
    def __init__(self):
        self._observers: List[Callable[[Any], Any]] = []

    def register_observer(self, observer: Callable[[Any], Any]):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer(event)

class PeriodicTimer:
    def __init__(self, cooldown: Millis):
        self.cooldown = cooldown
        self.time_until_next_run = cooldown

    def update_and_check_if_ready(self, time_passed: Millis) -> bool:
        self.time_until_next_run -= time_passed
        if self.time_until_next_run <= 0:
            self.time_until_next_run += self.cooldown
            return True
        return False


def get_all_directions():
    return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]