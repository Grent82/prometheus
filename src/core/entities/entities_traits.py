from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import random

from src.core.entities.entity_pathfinder import EntityPathfinder
from src.core.entities.game_entity import WorldEntity
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.common import Direction, Millis, PeriodicTimer, get_all_directions, get_perpendicular_directions
if TYPE_CHECKING:
    from src.core.npc import NonPlayerCharacter
    from src.core.states.game_state import GameState

class Trait:
    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        raise Exception("Must be overridden by sub-class!")
    
    
class RandomWalkTrait(Trait):
    def __init__(self, interval: Millis):
        self._timer = PeriodicTimer(interval)

    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        pass

    def update(self, npc: NonPlayerCharacter, time_passed: Millis):
        if self._timer.update_and_check_if_ready(time_passed):
            if random.random() < 0.8:
                npc.world_entity.set_not_moving()
            else:
                direction = random.choice(get_all_directions())
                npc.world_entity.set_moving_in_dir(direction)

class WalkTrait(Trait):
    def __init__(self, global_path_finder: GlobalPathFinder):
        self.random_walk_trait = RandomWalkTrait()
        self.pathfinder = EntityPathfinder(global_path_finder)
        self.next_waypoint: Tuple[int, int] = None
        self._reevaluate_next_waypoint_direction_interval = 1000
        self._time_since_reevaluated = self._reevaluate_next_waypoint_direction_interval
        self._time_since_updated_path = 0
        self._update_path_interval = 0

    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        pass

    def move_npc_to_target(self, game_state: GameState, npc: NonPlayerCharacter, target: NonPlayerCharacter):
        if self._time_since_updated_path > self._update_path_interval:
            self._time_since_updated_path = 0
            self.pathfinder.update_path_towards_target(npc.world_entity, game_state, target.world_entity)

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
                if random.random() < 0.5 and direction:
                    direction = random.choice(get_perpendicular_directions(direction))
                self._move_in_dir(npc.world_entity, direction)
            else:
                npc.world_entity.set_not_moving()
    
    def _move_in_dir(self, enemy_entity: WorldEntity, direction: Direction):
        if direction:
            enemy_entity.set_moving_in_dir(direction)
        else:
            enemy_entity.set_not_moving()

class TalkTrait(Trait):
    def __init__(self):
        pass

    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        conversation = self._get_npc_conversation(game_state, npc)
        if conversation:
            conversation.update(game_state.game_world, npc.agent, time_passed)

    def _get_npc_conversation(self, game_state: GameState, npc: NonPlayerCharacter):
        conversation = [c for c in game_state.game_world.conversations if c.is_member_of_conversation(npc.agent)]
        if conversation:
            return conversation[0]
        else:
            return None