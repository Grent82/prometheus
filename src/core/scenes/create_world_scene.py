from typing import Optional

from src.core.common import Millis
from src.core.scenes.abstract_scene import AbstractSceneFactory, AbstractScene, SceneTransition
from src.core.states.game_world_state import GameWorldState
from src.core.states.game_state import GameState

class CreatingWorldScene(AbstractScene):
    def __init__(self, scene_factory: AbstractSceneFactory):
        self.scene_factory = scene_factory

    def run_one_frame(self, _time_passed: Millis) -> Optional[SceneTransition]:

        #path_finder = init_global_path_finder()
        #game_state = self._setup_game_state(map_file_path)
        #path_finder.set_grid(game_state.pathfinder_wall_grid)

        return SceneTransition(None)

    def _setup_game_state(self) -> GameState:
        game_world = GameWorldState([], [], [])
        return GameState(game_world)