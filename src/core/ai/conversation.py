from enum import Enum
from typing import List, Optional

from src.core.ai.agent import Agent
from src.core.common import Millis
from src.core.entities.register_entity import NpcMind
from src.core.id_types import GameId, create_id
from src.core.math import get_manhattan_distance
from src.core.npc import NonPlayerCharacter
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.states.game_state import GameState
from src.core.states.game_world_state import GameWorldState

class ConversationStatus(Enum):
    INVITED: 0
    WALKING_OVER: 1
    PARTICIPATING: 2

class ConversationParticipant:
    def __init__(self, npc: NonPlayerCharacter, invited: Millis, status: ConversationStatus) -> None:
        self.npc = npc
        self.invited = invited
        self.status = status

class Typing:
    def __init__(self, npc_id: GameId, message_uuid:str, since: Millis) -> None:
        self.npc_id = npc_id
        self.message_uuid = message_uuid
        self.since = since

class Conversation:
    def __init__(self, creator: Agent, created: Millis, participants: List[ConversationParticipant]) -> None:
        self.id = create_id('conversations')
        self.creator = creator
        self.created = created
        self.participants = participants
        self.is_typing = Optional[Typing]
        self.last_message = None

    @staticmethod
    def start_conversation(game_world: GameWorldState, invitor: NonPlayerCharacter, invitee: NonPlayerCharacter, invited: Millis):
        if invitor.id == invitee.id:
            raise Exception("Can't invite yourself to a conversation")
    
        # ToDo: check if already in conversation
        
        invitor_participant = ConversationParticipant(invitor, invited, ConversationStatus.WALKING_OVER)
        invitee_participant = ConversationParticipant(invitee, invited, ConversationStatus.INVITED)
        participants = [invitor_participant, invitee_participant]

        conversation = Conversation(invitor, invited, participants)
        game_world.conversations.append(conversation)

        return conversation.id

    def stop_conversation(self, game_world: GameWorldState, now: Millis):
        self.is_typing = None

        for agent in game_world.agents:
            if agent.id == self.creator.id:
                agent.last_conversation = now
                agent.conversation_to_remember = self.id

        for c in game_world.conversations:
            if c.id == self.id:
                game_world.conversations.remove(c)
        
    def leave_conversation(self, game_world: GameWorldState, now: Millis):
        self.stop_conversation(game_world, now)

    def update(self, _time_passed: Millis):

        invitor = self.participants[0]
        invitee = self.participants[1]

        distance = get_manhattan_distance(invitor.npc.world_entity.get_position(), invitee.npc.world_entity.get_position())

    def accept_invite(self, participant: ConversationParticipant):
        participant.status = ConversationStatus.WALKING_OVER
    
    def reject_invite(self, participant: ConversationParticipant, game_world: GameWorldState, now: Millis):
        self.stop_conversation(game_world, now)

    def set_is_typing(self, message_uuid:str, now: Millis):
        if self.is_typing:
            return
        self.is_typing = Typing(self.creator.id, message_uuid, now)


    def is_member_of_conversation(self, agent:Agent):
        return [npc for npc in self.get_members_of_conversation() if npc.agent.id == agent.id] != None
    
    def get_members_of_conversation(self):
        return [p.npc for p in self.participants]
    
    def get_conversation_participant(self, npc: NonPlayerCharacter):
        for p in self.participants:
            if p.npc.agent.id == npc.agent.id:
                return p
        raise Exception("Can't find participant in conversation")
    
    def get_other_conversation_participant(self, npc: NonPlayerCharacter):
        for p in self.participants:
            if p.npc.agent.id != npc.agent.id:
                return p
        raise Exception("No other participant in conversation")
        