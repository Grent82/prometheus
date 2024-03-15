import sys
from typing import Optional, List, Any

import pygame

from src.core.common import Millis
from src.core.game_data import ENTITY_SPRITE_INITIALIZERS
from src.core.views.game_ui_view import GameUiView
from src.core.views.game_world_view import GameWorldView
from src.core.views.image_loading import load_images_by_sprite
from src.core.scenes.abstract_scene import AbstractScene, SceneTransition
from src.core.scenes.scene_factory import SceneFactory
from src.core.scenes.create_world_scene import CreatingWorldScene

SCREEN_SIZE = (800, 600)  # If this is not a supported resolution, performance takes a big hit
CAMERA_SIZE = (800, 430)

class Main:
    def __init__(self, fullscreen: bool):
        
        pygame.init()

        self.fullscreen = fullscreen
        self.pygame_screen = self.setup_screen()

        images_by_sprite = load_images_by_sprite(ENTITY_SPRITE_INITIALIZERS)
        
        self.world_view = GameWorldView(self.pygame_screen, CAMERA_SIZE, SCREEN_SIZE, images_by_sprite)
        self.ui_view = GameUiView()

        self.clock = pygame.time.Clock()

        self.scene_factory = SceneFactory(self.pygame_screen, self.ui_view, self.world_view, self.toggle_fullscreen, CAMERA_SIZE)

        self.scene: AbstractScene = CreatingWorldScene(self.scene_factory)

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
            #fps_string = str(int(round(self.clock.get_fps())))

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

    def change_scene(self, scene_transition: SceneTransition):
        self.scene = scene_transition.scene
        self.scene.on_enter()


def start(fullscreen: bool):
    main = Main(fullscreen)
    main.main_loop()

if __name__ == "__main__":
    start(fullscreen=False)