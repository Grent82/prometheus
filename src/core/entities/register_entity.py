from __future__ import annotations
from typing import TYPE_CHECKING

from src.core.entities.behaviors.entity_behaviors import TalkingNpcMind
if TYPE_CHECKING:
    from src.core.npc import NonPlayerCharacter
    from src.core.states.game_state import GameState

from src.core.common import Direction, Millis, NpcType, Sprite
from src.core.entities.entities_traits import RandomWalkTrait, TalkTrait, WalkTrait
from src.core.entities.entity_behavior import AbstractNpcMind, register_npc_behavior
from src.core.game_data import NpcData, register_entity_sprite_map, register_npc_data
from src.core.pathfinding.pathfinder import GlobalPathFinder
from src.core.views.image_loading import SpriteSheet


class NpcMind(AbstractNpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder):
        super().__init__(global_path_finder)
        self.talk_trait = TalkTrait()
        self.walk_trait = WalkTrait(global_path_finder)

    def control_npc(self, npc: NonPlayerCharacter, game_state: GameState, time_passed: Millis):
         self.talk_trait.update(npc, game_state, time_passed)
         self.walk_trait.move_npc_to_target(game_state, npc, None)


def register_male_npc():
    size = (30, 30)
    sprite = Sprite.NPC
    npc_type = NpcType.MALE
    npc_data = NpcData(sprite, size, speed=0.03)
    register_npc_data(npc_type, npc_data)
    register_npc_behavior(npc_type, NpcMind)

    sprite_sheet = SpriteSheet("resources/graphics/npc_sprite_sheet.png") # ToDo change me
    original_sprite_size = (32, 32)
    scaled_sprite_size = (48, 48)
    # ToDo set correct values
    indices_by_dir = {
        Direction.DOWN: [(0, 4), (1, 4), (2, 4)],
        Direction.LEFT: [(0, 5), (1, 5), (2, 5)],
        Direction.RIGHT: [(0, 6), (1, 6), (2, 6)],
        Direction.UP: [(0, 7), (1, 7), (2, 7)]
    }
    # ToDo fix relative
    register_entity_sprite_map(sprite, sprite_sheet, original_sprite_size, scaled_sprite_size, indices_by_dir, (-8, -16))

def register_female_npc():
    size = (30, 30)
    sprite = Sprite.NPC
    npc_type = NpcType.FEMALE
    npc_data = NpcData(sprite, size)
    register_npc_data(npc_type, npc_data, speed=0.03)
    register_npc_behavior(npc_type, NpcMind)

    sprite_sheet = SpriteSheet("resources/graphics/npc_sprite_sheet.png") # ToDo change me
    original_sprite_size = (32, 32)
    scaled_sprite_size = (48, 48)
    # ToDo set correct values
    indices_by_dir = {
        Direction.DOWN: [(0, 4), (1, 4), (2, 4)],
        Direction.LEFT: [(0, 5), (1, 5), (2, 5)],
        Direction.RIGHT: [(0, 6), (1, 6), (2, 6)],
        Direction.UP: [(0, 7), (1, 7), (2, 7)]
    }
    # ToDo fix relative
    register_entity_sprite_map(sprite, sprite_sheet, original_sprite_size, scaled_sprite_size, indices_by_dir, (-8, -16))