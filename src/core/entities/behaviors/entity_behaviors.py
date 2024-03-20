

import random
from typing import List, Optional, Tuple
from src.core.ai import conversation
from src.core.ai.conversation import Conversation, ConversationStatus
from src.core.common import Direction, Millis
from src.core.entities.entities_trait import RandomWalkTrait
from src.core.entities.behaviors.entity_behavior import AbstractNpcMind
from src.core.entities.entity_pathfinder import EntityPathfinder
from src.core.entities.game_entity import WorldEntity
from src.core.id_types import GameId
from src.core.math import get_manhattan_distance, get_perpendicular_directions
from src.core.npc import NonPlayerCharacter
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.states.game_state import GameState

ACTION_TIMEOUT:Millis = 60 * 10000
INVITE_TIMEOUT: Millis = 60 * 10000
INVITE_ACCEPT_PROBABILITY: float = 0.8
CONVERSATION_DISTANCE: float = 1.69


class Operation:
    def __init__(self, name: str, operation_id: str, started: Millis) -> None:
        self.name = name
        self.operation_id = operation_id
        self.started = started


class NpcMind(AbstractNpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder):
        self.random_walk_trait = RandomWalkTrait()

    def control_npc(self, game_state: GameState, npc: NonPlayerCharacter, time_passed: Millis):
        self.random_walk_trait.update(self, npc, game_state, time_passed)

class MovingNpcMind(NpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder):
        super().__init__(global_path_finder)
        self.pathfinder = EntityPathfinder(global_path_finder)
        self.next_waypoint: Tuple[int, int] = None
        self._time_since_updated_path = 0
        self._time_since_reevaluated = 0
        self._update_path_interval = 0
        

    def control_npc(self, game_state: GameState, npc: NonPlayerCharacter, now: Millis):
        pass

    def move_npc_to_target(self, game_state: GameState, npc: NonPlayerCharacter, target: NonPlayerCharacter):
        if self._time_since_updated_path > self._update_path_interval:
            self._time_since_updated_path = 0
            self.pathfinder.update_path_towards_target(npc.world_entity, game_state, self.target.world_entity)

        new_next_waypoint = self.pathfinder.get_next_waypoint_along_path(npc.world_entity)

        should_update_waypoint = self.next_waypoint != new_next_waypoint
        if self._time_since_reevaluated > self._reevaluate_next_waypoint_direction_interval:
            self._time_since_reevaluated = 0
            should_update_waypoint = True

        if should_update_waypoint:
            self.next_waypoint = new_next_waypoint
            if self.next_waypoint:
                direction = self.pathfinder.get_dir_towards_considering_collisions(
                    game_state, npc.world_entity, self.next_waypoint)
                if random.random() < self.chance_to_stray_from_path and direction:
                    direction = random.choice(get_perpendicular_directions(direction))
                self._move_in_dir(npc.world_entity, direction)
            else:
                npc.world_entity.set_not_moving()
    
    def _move_in_dir(self, enemy_entity: WorldEntity, direction: Direction):
        if direction:
            enemy_entity.set_moving_in_dir(direction)
        else:
            enemy_entity.set_not_moving()


class TalkingNpcMind(MovingNpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder, 
                 conversation_to_remember: Optional[GameId], 
                 last_conversation: Optional[Millis], 
                 last_conversation_invite_attempt: Optional[Millis]):
        super().__init__(global_path_finder)
        self.conversation_to_remember = conversation_to_remember # when loading a saved game
        self.last_conversation = last_conversation
        self.last_conversation_invite_attempt = last_conversation_invite_attempt
        self.in_progress_operation: Operation = None

    def control_npc(self, game_state: GameState, npc: NonPlayerCharacter, now: Millis):
        if self.in_progress_operation:
            if now < self.in_progress_operation.started + ACTION_TIMEOUT:
                return
            else:
                self.in_progress_operation = None
        
        conversation = self._get_npc_conversation(game_state, npc)
        
        if conversation:
            participant = conversation.get_conversation_participant(npc)
            other_participant = conversation.get_other_conversation_participant(npc)

            #if self.conversation_to_remember:
            #    todo: load data from db

            if participant.status == ConversationStatus.INVITED:
                if random.random() < INVITE_ACCEPT_PROBABILITY: # ToDo other participant is human?
                    conversation.accept_invite(participant)
                    npc.world_entity.set_not_moving()
                else:
                    conversation.reject_invite(participant, game_state.game_world)
                return
            if participant.status == ConversationStatus.WALKING_OVER:
                if participant.invited + INVITE_TIMEOUT < now:
                    conversation.leave_conversation(game_state.game_world, now)
                    return
                
                distance = get_manhattan_distance(participant.npc.world_entity.get_position(), other_participant.npc.world_entity.get_position())
                if distance < CONVERSATION_DISTANCE:
                    return

                super().move_npc_to_target(game_state, participant.npc, other_participant.npc)
                return
            if participant.status == ConversationStatus.PARTICIPATING:
                pass
                
                




    def _get_npc_conversation(self, game_state: GameState, npc: NonPlayerCharacter):
        conversation = [c for c in game_state.game_world.conversations if c.is_member_of_conversation(npc.agent)]
        if conversation:
            return conversation[0]
        else:
            return None
        