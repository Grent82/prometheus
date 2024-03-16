from typing import List, Any, Optional

from src.core.common import Millis
from src.core.game_engine import GameEngine
from src.core.states.game_state import GameState
from src.core.views.game_ui_view import GameUiView

class SceneTransition:
    # scene: AbstractScene
    def __init__(self, scene):
        self.scene = scene

class AbstractScene:
    def on_enter(self):
        pass
    def handle_user_input(self, events: List[Any]) -> Optional[SceneTransition]:
        pass
    def run_one_frame(self, _time_passed: Millis) -> Optional[SceneTransition]:
        pass
    def render(self):
        pass

class AbstractSceneFactory:

    def main_menu_scene(self) -> AbstractScene:
        raise Exception("Not implemented")

    def world_scene(self) -> AbstractScene:
        raise Exception("Not implemented")
    
    def playing_scene(self, game_state: GameState, game_engine: GameEngine, ui_view: GameUiView) -> AbstractScene:
        raise Exception("Not implemented")