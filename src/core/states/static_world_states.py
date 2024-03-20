from typing import Any, Dict, List, Tuple

from pygame import Rect

from src.core.entities.game_entity import WorldEntity
from src.core.entities.static_world_entites import StaticWorldEntity


class StaticWorldEntityState:
    def __init__(self, static_world_entities: List[StaticWorldEntity], entire_world_area: Rect):
        self.static_world_entities: List[StaticWorldEntity] = static_world_entities
        self._buckets = Buckets([w.world_entity for w in static_world_entities], entire_world_area)
        self._entire_world_area = entire_world_area

    def add_static_world_entity(self, static_world_entity: StaticWorldEntity):
        self.static_world_entities.append(static_world_entity)
        self._buckets.add_entity(static_world_entity.world_entity)

    def remove_static_world_entity(self, static_world_entity: StaticWorldEntity):
        self.static_world_entities.remove(static_world_entity)
        self._buckets.remove_entity(static_world_entity.world_entity)

    def remove_all_from_position(self, position: Tuple[int, int]):
        for static_world_entity in self.get_static_world_entities_at_position(position):
            self.remove_static_world_entity(static_world_entity)

    def clear(self):
        self.static_world_entities.clear()
        self._buckets = Buckets([], self._entire_world_area)

    def does_rect_intersect_with_static_world_entity(self, rect: Rect):
        nearby_static_world_entities = self.get_static_world_entities_close_to_position((rect[0], rect[1]))
        return any([static_world_entity for static_world_entity in nearby_static_world_entities if static_world_entity.check_collision(rect)])

    def get_static_world_entities_close_to_position(self, position: Tuple[int, int]) -> List[WorldEntity]:
        return self._buckets.get_entities_close_to_position(position)

    def get_static_world_entities_in_camera(self, camera_world_area: Rect) -> List[WorldEntity]:
        return self._buckets.get_entitites_close_to_world_area(camera_world_area)

    def get_static_world_entities_at_position(self, position: Tuple[int, int]) -> List[StaticWorldEntity]:
        return [w for w in self.static_world_entities if w.world_entity.get_position() == position]
    

class Buckets:
    _BUCKET_WIDTH = 100
    _BUCKET_HEIGHT = 100

    def __init__(self, entities: List[Any], entire_world_area: Rect):
        self._buckets: Dict[int, Dict[int, List[Any]]] = {}
        self.entire_world_area = entire_world_area
        for x_bucket in range(self.entire_world_area.w // Buckets._BUCKET_WIDTH + 1):
            self._buckets[x_bucket] = {}
            for y_bucket in range(self.entire_world_area.h // Buckets._BUCKET_HEIGHT + 1):
                self._buckets[x_bucket][y_bucket] = []
        for entity in entities:
            self.add_entity(entity)

    def add_entity(self, entity: Any):
        bucket = self._bucket_for_world_position(entity.get_position())
        bucket.append(entity)

    def remove_entity(self, entity: Any):
        bucket = self._bucket_for_world_position(entity.get_position())
        bucket.remove(entity)

    def get_entitites_close_to_world_area(self, world_area: Rect) -> List[Any]:
        x0_bucket, y0_bucket = self._bucket_index_for_world_position(world_area.topleft)
        x1_bucket, y1_bucket = self._bucket_index_for_world_position(world_area.bottomright)
        buckets = self._buckets_between_indices(x0_bucket - 1, x1_bucket + 1, y0_bucket - 1, y1_bucket + 1)
        return [entity for bucket in buckets for entity in bucket]

    def get_entities_close_to_position(self, position: Tuple[int, int]) -> List[Any]:
        x_bucket, y_bucket = self._bucket_index_for_world_position(position)
        buckets = self._buckets_between_indices(x_bucket - 1, x_bucket + 1, y_bucket - 1, y_bucket + 1)
        return [entity for bucket in buckets for entity in bucket]

    def _buckets_between_indices(self, x0: int, x1: int, y0: int, y1: int) -> List[List[Any]]:
        for x_bucket in range(max(0, x0), min(x1 + 1, len(self._buckets))):
            for y_bucket in range(max(0, y0), min(y1 + 1, len(self._buckets[x_bucket]))):
                yield self._buckets[x_bucket][y_bucket]

    def _bucket_for_world_position(self, world_position: Tuple[int, int]):
        x_bucket, y_bucket = self._bucket_index_for_world_position(world_position)
        return self._buckets[x_bucket][y_bucket]

    def _bucket_index_for_world_position(self, world_position: Tuple[int, int]) -> Tuple[int, int]:
        x_bucket = int(world_position[0] - self.entire_world_area.x) // Buckets._BUCKET_WIDTH
        y_bucket = int(world_position[1] - self.entire_world_area.y) // Buckets._BUCKET_HEIGHT
        return x_bucket, y_bucket