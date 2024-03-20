

from typing import Dict, Type
from src.core.common import Millis, NpcType
from src.core.entities.game_entity import WorldEntity
from src.core.npc import NonPlayerCharacter
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.states.game_state import GameState

class AbstractNpcMind:

    def __init__(self, _global_path_finder: GlobalPathFinder):
        pass

    def control_npc(self,
                    game_state: GameState,
                    npc: NonPlayerCharacter,
                    time_passed: Millis):
        pass

    # ToDo combine AI behavior here
    

_npc_mind_constructors: Dict[NpcType, Type[AbstractNpcMind]] = {}


def create_npc_mind(npc_type: NpcType, global_path_finder: GlobalPathFinder):
    constructor = _npc_mind_constructors[npc_type]
    return constructor(global_path_finder)

def register_npc_behavior(npc_type: NpcType, mind_constructor: Type[AbstractNpcMind]):
    _npc_mind_constructors[npc_type] = mind_constructor
