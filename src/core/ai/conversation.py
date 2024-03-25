from enum import Enum
import random
from typing import List, Optional
import uuid

from src.core.ai.agent import Agent
from src.core.ai.agent_operations import AsyncMessageTask, AsyncMessageTasktype
from src.core.common import Millis
from src.core.id_types import GameId, create_id
from src.core.states.game_world_state import GameWorldState

ACTION_TIMEOUT:Millis = 60 * 10000
INVITE_TIMEOUT: Millis = 60 * 10000
INVITE_ACCEPT_PROBABILITY: float = 0.8
CONVERSATION_DISTANCE: float = 1.69
AWKWARD_CONVERSATION_TIMEOUT: Millis = 2 * 10000
MESSAGE_COOLDOWN: Millis = 2000

class ConversationStatus(Enum):
    INVITED: 0
    WALKING_OVER: 1
    PARTICIPATING: 2

class ConversationParticipant:
    def __init__(self, agent: Agent, invited: Millis, status: ConversationStatus) -> None:
        self.agent = agent
        self.invited = invited
        self.status = status
        self.started = Optional[Millis]

class ConversationMessage:
    def __init__(self, agent: Agent, now: Millis) -> None:
        self.author = agent
        self.timestamp = now

class Typing:
    def __init__(self, agent_id: GameId, message_uuid:str, since: Millis) -> None:
        self.agent_id = agent_id
        self.message_uuid = message_uuid
        self.since = since



class Conversation:
    def __init__(self, creator: Agent, created: Millis, participants: List[ConversationParticipant]) -> None:
        self.id = create_id('conversations')
        self.creator = creator
        self.created = created
        self.participants = participants
        self.is_typing: Typing = Optional[Typing]
        self.last_message: ConversationMessage = Optional[ConversationMessage]

    @staticmethod
    def start(game_world: GameWorldState, invitor: Agent, invitee: Agent, invited: Millis):
        if invitor.id == invitee.id:
            raise Exception("Can't invite yourself to a conversation")
    
        # ToDo: check if already in conversation
        
        invitor_participant = ConversationParticipant(invitor, invited, ConversationStatus.WALKING_OVER)
        invitee_participant = ConversationParticipant(invitee, invited, ConversationStatus.INVITED)
        participants = [invitor_participant, invitee_participant]

        conversation = Conversation(invitor, invited, participants)
        game_world.conversations.append(conversation)

        return conversation.id

    def stop(self, game_world: GameWorldState, now: Millis):
        self.is_typing = None

        for agent in game_world.agents:
            if agent.id == self.creator.id:
                agent.last_conversation = now
                agent.conversation_to_remember = self.id

        for c in game_world.conversations:
            if c.id == self.id:
                game_world.conversations.remove(c)
        
    def leave(self, game_world: GameWorldState, now: Millis):
        self.stop(game_world, now)


    def update(self, game_world: GameWorldState, npc:Agent, now: Millis):
        participant = self.get_conversation_participant(npc)
        other_participant = self.get_other_conversation_participant(npc)

        #if self.conversation_to_remember:
        #    todo: load data from db

        if participant.status == ConversationStatus.INVITED:
            if random.random() < INVITE_ACCEPT_PROBABILITY: # ToDo other participant is human?
                self.accept_invite(participant)
            else:
                self.reject_invite(participant, game_world)
        elif participant.status == ConversationStatus.WALKING_OVER:
            if participant.invited + INVITE_TIMEOUT < now:
                self.leave(game_world, now)
            
            # ToDo handle moving to participant
        
        elif participant.status == ConversationStatus.PARTICIPATING:
            started = participant.started

            if self.is_typing and self.is_typing.agent_id == participant.agent.id:
                msg_uuid = str(uuid.uuid4())
                self.set_is_typing(Typing(participant.agent.id, msg_uuid, now))
                participant.agent.agent_operation_handler.process_task(
                    AsyncMessageTask(participant.agent.id, other_participant.agent.id, self.id, msg_uuid, AsyncMessageTasktype.CONTINUE))
                
            elif not self.last_message:
                is_initiator = self.creator == participant.agent.id
                awkward_deadline = started + AWKWARD_CONVERSATION_TIMEOUT

                if is_initiator or awkward_deadline < now:
                    msg_uuid = str(uuid.uuid4())
                    self.set_is_typing(Typing(participant.agent.id, msg_uuid, now))
                    participant.agent.agent_operation_handler.process_task(
                        AsyncMessageTask(participant.agent.id, other_participant.agent.id, self.id, msg_uuid, AsyncMessageTasktype.START))
                
            else:
                if self.last_message.author.id == participant.agent.id:
                    awkward_deadline = started + AWKWARD_CONVERSATION_TIMEOUT
                    if now < awkward_deadline:
                        return
                else:
                    message_cooldown = self.last_message.timestamp + MESSAGE_COOLDOWN    
                    if now < message_cooldown:
                        return
                    
            

    def accept_invite(self, participant: ConversationParticipant):
        participant.status = ConversationStatus.WALKING_OVER
    
    def reject_invite(self, game_world: GameWorldState, now: Millis):
        self.stop(game_world, now)

    def set_is_typing(self, message_uuid:str, now: Millis):
        if self.is_typing:
            return
        self.is_typing = Typing(self.creator.id, message_uuid, now)


    def is_member_of_conversation(self, agent:Agent):
        return [a for a in self.get_members_of_conversation() if a.id == agent.id] != None
    
    def get_members_of_conversation(self):
        return [p.agent for p in self.participants]
    
    def get_conversation_participant(self, agent:Agent):
        for p in self.participants:
            if p.id == agent.id:
                return p
        raise Exception("Can't find participant in conversation")
    
    def get_other_conversation_participant(self, agent:Agent):
        for p in self.participants:
            if p.agent.id != agent.id:
                return p
        raise Exception("No other participant in conversation")
        