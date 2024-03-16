from typing import List

from pygame import Rect
from src.core import game_entity
from src.core.game_entity import WorldEntity
from src.ai.agent import Agent
from src.ai.conversation import Conversation
from src.core.id_types import GameId, create_id

class GameWorldState:
    def __init__(self, entities: List[WorldEntity], agents:List[Agent], conversations:List[Conversation]):
        self.id: GameId = create_id('Worlds')
        self.entities = entities
        self.agents = agents
        self.conversations = conversations

        self.entire_world_area = Rect((0, 0), (500, 500)) # change me

    def add_entity(self, npc: game_entity):
        self.entities.append(npc)

    def get_renderable_entities(self) -> List[WorldEntity]:
        return [e.world_entity for e in self.entities]
