from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.npc import NonPlayerCharacter
    from src.core.states.game_state import GameState

import random

from src.core.common import Millis, PeriodicTimer, get_all_directions


class Trait:
    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        raise Exception("Must be overridden by sub-class!")
    
    
class RandomWalkTrait(Trait):
    def __init__(self, interval: Millis):
        self._timer = PeriodicTimer(interval)

    def update(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
        if self._timer.update_and_check_if_ready(time_passed):
            if random.random() < 0.8:
                npc.world_entity.set_not_moving()
            else:
                direction = random.choice(get_all_directions())
                npc.world_entity.set_moving_in_dir(direction)