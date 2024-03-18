from typing import List

from pygame import Rect
from src.core.entities import game_entity
from src.core.entities.game_entity import WorldEntity
from src.ai.agent import Agent
from src.ai.conversation import Conversation
from src.core.id_types import GameId, create_id
from src.core.entities.world_entites import StaticWorldEntity
from src.core.states.static_world_states import StaticWorldEntityState

class GameWorldState:
    def __init__(self, entire_world_area: Rect, static_entites: List[StaticWorldEntity], entities: List[WorldEntity], agents:List[Agent], conversations:List[Conversation]):
        self.id: GameId = create_id('Worlds')

        self.entire_world_area = entire_world_area
        self.static_entites = StaticWorldEntityState(static_entites, entire_world_area)

        self.entities = entities
        self.agents = agents
        self.conversations = conversations

        

    def add_entity(self, npc: game_entity):
        self.entities.append(npc)

    def get_renderable_entities(self) -> List[WorldEntity]:
        return [e.world_entity for e in self.entities]
