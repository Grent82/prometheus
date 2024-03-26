
from typing import Optional
from src.core.ai.agent_operations import AsyncOperationHandler
from src.core.common import Millis
from src.core.id_types import GameId, create_id, GAME_ID_TYPES

class Agent:
    def __init__(self, conversation_to_remember: Optional[GameId], last_conversation: Optional[Millis]) -> None:
        self.id = create_id('agents').id
        self.conversation_to_remember = conversation_to_remember
        self.last_conversation = last_conversation
        self.agent_operation_handler = AsyncOperationHandler()