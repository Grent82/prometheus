from typing import Tuple, Callable

class DrawableArea:
    def __init__(self, screen, translate_coordinates: Callable[[Tuple[int, int]], Tuple[int, int]] = lambda pos: pos):
        self.screen = screen
        self.translate_coordinates = translate_coordinates

    def fill(self, color: Tuple[int, int, int]):
        self.screen.fill(color)
