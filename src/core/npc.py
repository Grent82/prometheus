

from typing import Optional
from src.core.ai.agent import Agent
from src.core.common import NpcType
from src.core.entities.game_entity import WorldEntity
from src.core.entities.register_entity import NpcMind


class NonPlayerCharacter:
    def __init__(self, npc_type: NpcType, world_entity: WorldEntity, agent: Agent,
                 npc_mind: NpcMind, max_distance_allowed_from_start_position: Optional[int]):
        self.npc_type = npc_type
        self.world_entity = world_entity
        self.agent = agent
        self.npc_mind = npc_mind
        self.start_position = world_entity.get_position()
        self.max_distance_allowed_from_start_position = max_distance_allowed_from_start_position