from typing import Dict, List, Tuple

import pygame
from pygame.rect import Rect

from src.core.common import Sprite, Direction
from src.core.game_data import ENTITY_SPRITE_INITIALIZERS
from src.core.entities.game_entity import WorldEntity
from src.core.views.image_loading import ImageWithRelativePosition
from src.core.views.render_util import DrawableArea

COLOR_BACKGROUND = (88 + 30, 72 + 30, 40 + 30)
COLOR_BACKGROUND_LINES = (93 + 30, 77 + 30, 45 + 30)
COLOR_RED = (250, 0, 0)

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
    
    def render_world(self, all_entities_to_render: List[WorldEntity],
                     camera_world_area, entities: List[WorldEntity], entire_world_area: Rect):
        self.camera_world_area = camera_world_area

        self.screen_render.fill(COLOR_BACKGROUND)
        self._world_ground(entire_world_area)

        all_entities_to_render.sort(key=lambda entry: (-entry.view_z, entry.y))

        for entity in all_entities_to_render:
            self._world_entity(entity)

        for npc in entities:
            npc_sprite_y_relative_to_entity = \
                ENTITY_SPRITE_INITIALIZERS[npc.sprite][Direction.DOWN].position_relative_to_entity[1]
            
    def _world_ground(self, entire_world_area: Rect):
        grid_width = 35
        # TODO num squares should depend on map size. Ideally this dumb looping logic should change.
        num_squares = 200
        column_screen_y_0 = self._translate_world_y_to_screen(self.camera_world_area.y)
        column_screen_y_1 = self._translate_world_y_to_screen(
            min(entire_world_area.y + entire_world_area.h, self.camera_world_area.y + self.camera_world_area.h))
        for i_col in range(num_squares):
            world_x = entire_world_area.x + i_col * grid_width
            if entire_world_area.x < world_x < entire_world_area.x + entire_world_area.w:
                screen_x = self._translate_world_x_to_screen(world_x)
                self.screen_render.line(COLOR_BACKGROUND_LINES, (screen_x, column_screen_y_0),
                                        (screen_x, column_screen_y_1),
                                        1)
        row_screen_x_0 = self._translate_world_x_to_screen(self.camera_world_area.x)
        row_screen_x_1 = self._translate_world_x_to_screen(
            min(entire_world_area.x + entire_world_area.w, self.camera_world_area.x + self.camera_world_area.w))
        for i_row in range(num_squares):
            world_y = entire_world_area.y + i_row * grid_width
            if entire_world_area.y < world_y < entire_world_area.y + entire_world_area.h:
                screen_y = self._translate_world_y_to_screen(world_y)
                self.screen_render.line(COLOR_BACKGROUND_LINES, (row_screen_x_0, screen_y), (row_screen_x_1, screen_y), 1)
                