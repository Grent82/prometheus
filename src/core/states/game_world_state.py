from typing import List

from pygame import Rect
from src.core.ai.agent import Agent
from src.core.ai.conversation import Conversation
from src.core.id_types import create_id
from src.core.entities.static_world_entites import StaticWorldEntity
from src.core.npc import NonPlayerCharacter
from src.core.states.static_world_states import StaticWorldEntityState

class GameWorldState:
    def __init__(self, entire_world_area: Rect, static_entites: List[StaticWorldEntity], non_player_characters: List[NonPlayerCharacter], conversations:List[Conversation]):
        self.id: int = create_id('worlds').id

        self.entire_world_area = entire_world_area
        self.static_entites = StaticWorldEntityState(static_entites, entire_world_area)

        self.non_player_characters = non_player_characters
        self.conversations = conversations

    
    def add_npc(self, npc: NonPlayerCharacter):
        self.non_player_characters.append(npc)

    def get_renderable_entities(self) -> List[NonPlayerCharacter]:
        return [npc.world_entity for npc in self.non_player_characters]
    
    def get_agents(self):
        return [npc.agent for npc in self.non_player_characters]
    
    def get_entity_of_agent(self, agent:Agent):
        for npc in self.non_player_characters:
            if npc.agent.id == agent.id:
                return npc.world_entity
        return None
    
    def update_move_target_of_agent(self, agent:Agent, target:Agent):
        for npc in self.non_player_characters:
            if npc.agent.id == agent.id:
                entity = self.get_entity_of_agent(agent)
                target_entity = self.get_entity_of_agent(target)
                npc.npc_mind.get_walk_trait().set_target(self, entity, target_entity)
