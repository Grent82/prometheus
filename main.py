import sys
from typing import Optional, List, Any

import pygame

from src.core.common import Millis
from src.core.game_data import ENTITY_SPRITE_INITIALIZERS
from src.core.views.game_world_view import GameWorldView
from src.core.views.image_loading import load_images_by_sprite

SCREEN_SIZE = (800, 600)  # If this is not a supported resolution, performance takes a big hit
CAMERA_SIZE = (800, 430)

class Main:
    def __init__(self, map_file_name: Optional[str], fullscreen: bool):
        
        pygame.init()

        self.fullscreen = fullscreen
        self.pygame_screen = self.setup_screen()
        images_by_sprite = load_images_by_sprite(ENTITY_SPRITE_INITIALIZERS)
        self.world_view = GameWorldView(self.pygame_screen, CAMERA_SIZE, SCREEN_SIZE, images_by_sprite)

        self.clock = pygame.time.Clock()

    def main_loop(self):
        try:
            self._main_loop()
        except Exception as e:
            print("Game crashed with an unexpected error! %s" % e)
            raise e
        
    def _main_loop(self):
        while True:
            self.clock.tick()
            time_passed = Millis(self.clock.get_time())
            fps_string = str(int(self.clock.get_fps()))

            input_events: List[Any] = pygame.event.get()
            for event in input_events:
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.fullscreen:
                    self.toggle_fullscreen()

            self.scene.render()
            pygame.display.update()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.pygame_screen = self.setup_screen()

    def setup_screen(self):
        flags = pygame.DOUBLEBUF
        if self.fullscreen:
            flags = flags | pygame.FULLSCREEN | pygame.HWSURFACE
        return pygame.display.set_mode(SCREEN_SIZE, flags)

    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    def change_scene(self):
        self.scene.on_enter()


def start(map_file_name: Optional[str], fullscreen: bool):
    main = Main(map_file_name, fullscreen)
    main.main_loop()