from typing import Any, Callable, List, Optional

from src.core.common import Millis
from src.core.game_engine import GameEngine
from src.core.scenes.abstract_scene import AbstractScene, AbstractSceneFactory, SceneTransition
from src.core.states.game_state import GameState
from src.core.views.game_ui_view import GameUiView
from src.core.views.game_world_view import GameWorldView


class PlayingScene(AbstractScene):
    def __init__(self,
                 scene_factory: AbstractSceneFactory,
                 world_view: GameWorldView,
                 game_state: GameState,
                 game_engine: GameEngine,
                 ui_view: GameUiView,
                 toggle_fullscreen_callback: Callable[[], Any]):

        self.scene_factory = scene_factory
        self.world_view = world_view
        self.game_state: GameState = game_state
        self.game_engine: GameEngine = game_engine
        self.ui_view: GameUiView = ui_view
        self.toggle_fullscreen_callback = toggle_fullscreen_callback

    def on_enter(self):
        pass

    def handle_user_input(self, events: List[Any]) -> Optional[SceneTransition]:
        pass
    
    def run_one_frame(self, time_passed: Millis) -> Optional[SceneTransition]:

        self.game_engine.run_one_frame(time_passed)

        self.ui_view.update(time_passed)

        return None
    
    def render(self):

        game_world = self.game_state.game_world
        self.world_view.render_world(
            all_entities_to_render = self.game_state.get_all_entities_to_render(),
            camera_world_area = self.game_state.get_camera_world_area(),
            entities = game_world.non_player_characters,
            entire_world_area = game_world.entire_world_area
            )
        
        self.ui_view.render()
