
from typing import Optional, Tuple

from src.core.common import Millis
from src.core.game_engine import GameEngine
from src.core.scenes.abstract_scene import AbstractSceneFactory, AbstractScene
from src.core.scenes.create_world_scene import CreatingWorldScene
from src.core.scenes.playing_scene import PlayingScene
from src.core.states.game_state import GameState
from src.core.views.game_world_view import GameWorldView
from src.core.views.game_ui_view import GameUiView

class SceneFactory(AbstractSceneFactory):

    def __init__(self, pygame_screen, ui_view: GameUiView, world_view: GameWorldView, toggle_fullscreen, camera_size: Tuple[int, int]):
        self.pygame_screen = pygame_screen
        self.ui_view = ui_view
        self.world_view = world_view
        self.toggle_fullscreen = toggle_fullscreen
        self.camera_size = camera_size

    def main_menu_scene(self) -> AbstractScene:
        pass

    def world_scene(self) -> AbstractScene:
        return CreatingWorldScene(self, self.camera_size, self.ui_view)

    def playing_scene(self, game_state: GameState, game_engine: GameEngine, ui_view: GameUiView) -> AbstractScene:
        return PlayingScene(self, self.world_view, game_state, game_engine, ui_view, self.toggle_fullscreen)