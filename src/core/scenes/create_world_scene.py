from src.core.scenes.abstract_scene import AbstractSceneFactory, AbstractScene
from src.core.states.game_world_state import GameWorldState
from src.core.states.game_state import GameState

class CreatingWorldScene(AbstractScene):
    def __init__(self, scene_factory: AbstractSceneFactory):
        self.scene_factory = scene_factory

    def _setup_game_state(self) -> GameState:
        game_world = GameWorldState([], [], [])
        return GameState(game_world)