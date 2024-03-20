from typing import Dict, List, Optional, Tuple

from src.core.ai.agent import Agent
from src.core.common import Direction, NpcType, Sprite, StaticWorldEntityType
from src.core.id_types import GameId, create_id
from src.core.views.image_loading import Animation, SpriteInitializer, SpriteMapInitializer, SpriteSheet

class StaticWorldEntityData:
    def __init__(self, sprite: Sprite, size: Tuple[int, int]):
        self.sprite = sprite
        self.size = size

class NpcData:
    def __init__(self, sprite: Sprite, size: Tuple[int, int], speed: float, max_distance_allowed_from_start_position: Optional[int]):
        self.sprite = sprite
        self.size = size
        self.speed = speed
        self.max_distance_allowed_from_start_position = max_distance_allowed_from_start_position



NON_PLAYER_CHARACTERS: Dict[NpcType, NpcData] = {}

STATIC_ENTITES: Dict[StaticWorldEntityType, StaticWorldEntityData] = {}

ENTITY_SPRITE_INITIALIZERS: Dict[Sprite, Dict[Direction, Animation]] = {}
ENTITY_SPRITE_SIZES: Dict[Sprite, Tuple[int, int]] = {}


def register_npc_data(npc_type: NpcType, npc_data: NpcData):
    NON_PLAYER_CHARACTERS[npc_type] = npc_data
    
def register_static_entities_data(static_world_entity_type: StaticWorldEntityType, static_world_entity_data: StaticWorldEntityData):
    STATIC_ENTITES[static_world_entity_type] = static_world_entity_data

def register_entity_sprite_initializer(sprite: Sprite, initializer: SpriteInitializer,
                                       position_relative_to_entity: Tuple[int, int] = (0, 0)):
    ENTITY_SPRITE_INITIALIZERS[sprite] = {Direction.DOWN: Animation([initializer], None, position_relative_to_entity)}
    ENTITY_SPRITE_SIZES[sprite] = initializer.scaling_size

def register_entity_sprite_map(
        sprite: Sprite,
        sprite_sheet: SpriteSheet,
        original_sprite_size: Tuple[int, int],
        scaled_sprite_size: Tuple[int, int],
        indices_by_dir: Dict[Direction, List[Tuple[int, int]]],
        position_relative_to_entity: Tuple[int, int]):
    
    initializers: Dict[Direction: SpriteMapInitializer] = {
        direction: [SpriteMapInitializer(sprite_sheet, original_sprite_size, scaled_sprite_size, index)
                    for index in indices_by_dir[direction]]
        for direction in indices_by_dir
    }
    
    ENTITY_SPRITE_INITIALIZERS[sprite] = {}
    for direction in initializers:
        if len(initializers[direction]) == 0:
            raise Exception("Invalid input: " + str(initializers))
        ENTITY_SPRITE_INITIALIZERS[sprite][direction] = Animation(
            None, initializers[direction], position_relative_to_entity)
    ENTITY_SPRITE_SIZES[sprite] = scaled_sprite_size
