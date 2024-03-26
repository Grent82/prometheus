

from typing import Tuple

from src.core.ai.agent import Agent
from src.core.common import Direction, NpcType
from src.core.entities.entity_behavior import create_npc_mind
from src.core.entities.game_entity import WorldEntity
from src.core.game_data import NON_PLAYER_CHARACTERS, NpcData
from src.core.id_types import create_id
from src.core.npc import NonPlayerCharacter
from src.core.pathfinding.pathfinder import get_global_path_finder


def create_npc(npc_type: NpcType, pos: Tuple[int, int]) -> NonPlayerCharacter:
    data: NpcData = NON_PLAYER_CHARACTERS[npc_type]
    entity = WorldEntity(create_id('npcs').id, pos, data.size, data.sprite, Direction.LEFT, data.speed)
    global_path_finder = get_global_path_finder()
    npc_mind = create_npc_mind(npc_type, global_path_finder)

    agent : Agent = Agent()

    return NonPlayerCharacter(npc_type, entity, agent, npc_mind, data.max_distance_allowed_from_start_position)