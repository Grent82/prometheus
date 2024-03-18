

from src.core.common import StaticWorldEntityType
from src.core.entities.game_entity import WorldEntity


class StaticWorldEntity:
    def __init__(self, static_type: StaticWorldEntityType, world_entity: WorldEntity):
        self.static_type = static_type
        self.world_entity = world_entity