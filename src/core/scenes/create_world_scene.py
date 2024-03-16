from typing import Optional, Tuple

from src.core.common import Millis
from src.core.game_engine import GameEngine
from src.core.scenes.abstract_scene import AbstractSceneFactory, AbstractScene, SceneTransition
from src.core.states.game_world_state import GameWorldState
from src.core.states.game_state import GameState
from src.core.views.game_ui_view import GameUiView

class CreatingWorldScene(AbstractScene):
    def __init__(self, scene_factory: AbstractSceneFactory, camera_size: Tuple[int, int], ui_view: GameUiView):
        self.scene_factory = scene_factory
        self.camera_size = camera_size
        self.ui_view = ui_view

    def run_one_frame(self, _time_passed: Millis) -> Optional[SceneTransition]:

        #path_finder = init_global_path_finder()
        game_state = self._setup_game_state()
        #path_finder.set_grid(game_state.pathfinder_wall_grid)

        game_engine = GameEngine(game_state)

        #self.ui_view.on_world_area_updated(game_state.game_world.entire_world_area)
        playing_scene = self.scene_factory.playing_scene(game_state, game_engine, self.ui_view)
        return SceneTransition(playing_scene)

    def _setup_game_state(self) -> GameState:
        game_world = GameWorldState([], [], [])
        return GameState(game_world, self.camera_size)