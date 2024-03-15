from enum import Enum
from typing import Dict, List, Tuple, Optional, Union

import pygame
from pygame.rect import Rect

from src.core.common import Sprite, Direction
from src.core.views.image_loading import ImageWithRelativePosition
from src.core.views.render_util import DrawableArea

class GameWorldView:

    def __init__(self, pygame_screen, camera_size: Tuple[int, int], screen_size: Tuple[int, int],
                 images_by_sprite: Dict[Sprite, Dict[Direction, List[ImageWithRelativePosition]]]):
        pygame.font.init()
        self.screen_render = DrawableArea(pygame_screen)
        self.ui_render = DrawableArea(pygame_screen, self._translate_ui_position_to_screen)
        self.world_render = DrawableArea(pygame_screen, self._translate_world_position_to_screen)

        self.ui_screen_area = Rect(0, camera_size[1], screen_size[0], screen_size[1] - camera_size[1])
        self.camera_size = camera_size
        self.screen_size = screen_size

        self.images_by_sprite: Dict[Sprite, Dict[Direction, List[ImageWithRelativePosition]]] = images_by_sprite

        self.camera_world_area = None
    
    
    def _translate_world_position_to_screen(self, world_position):
        return (self._translate_world_x_to_screen(world_position[0]),
                self._translate_world_y_to_screen(world_position[1]))

    def _translate_screen_position_to_world(self, screen_position):
        return int(screen_position[0] + self.camera_world_area.x), int(screen_position[1] + self.camera_world_area.y)

    def _translate_world_x_to_screen(self, world_x):
        return int(world_x - self.camera_world_area.x)

    def _translate_world_y_to_screen(self, world_y):
        return int(world_y - self.camera_world_area.y)

    def _translate_ui_position_to_screen(self, position):
        return position[0] + self.ui_screen_area.x, position[1] + self.ui_screen_area.y

    def _translate_screen_position_to_ui(self, position: Tuple[int, int]):
        return position[0] - self.ui_screen_area.x, position[1] - self.ui_screen_area.y