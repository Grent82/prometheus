
from enum import Enum
from typing import NewType, Any, List, Callable

Millis = NewType('Millis', int)

class Sprite(Enum):
    NONE: 0

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class Observable:
    def __init__(self):
        self._observers: List[Callable[[Any], Any]] = []

    def register_observer(self, observer: Callable[[Any], Any]):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer(event)