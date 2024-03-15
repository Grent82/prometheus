from typing import List
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
