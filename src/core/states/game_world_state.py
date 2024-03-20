from typing import List

from pygame import Rect
from src.core.entities import game_entity
from src.core.entities.game_entity import WorldEntity
from src.core.ai.agent import Agent
from src.core.ai.conversation import Conversation
from src.core.id_types import GameId, create_id
from src.core.entities.static_world_entites import StaticWorldEntity
from src.core.npc import NonPlayerCharacter
from src.core.states.static_world_states import StaticWorldEntityState

class GameWorldState:
    def __init__(self, entire_world_area: Rect, static_entites: List[StaticWorldEntity], non_player_characters: List[NonPlayerCharacter], agents:List[Agent], conversations:List[Conversation]):
        self.id: GameId = create_id('Worlds')

        self.entire_world_area = entire_world_area
        self.static_entites = StaticWorldEntityState(static_entites, entire_world_area)

        self.non_player_characters = non_player_characters
        self.agents = agents
        self.conversations = conversations

        

    def add_npc(self, npc: NonPlayerCharacter):
        self.non_player_characters.append(npc)

    def get_renderable_entities(self) -> List[NonPlayerCharacter]:
        return [e.world_entity for e in self.non_player_characters]
