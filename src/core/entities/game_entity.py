from typing import Tuple, Optional

from pygame.rect import Rect

from src.core.id_types import GameId
from src.core.common import Sprite, Direction, Observable

class WorldEntity:
    def __init__(self, id:GameId, pos: Tuple[int, int], size: Tuple[int, int], sprite: Sprite, direction=Direction.LEFT, speed:int=0):
        self.id: GameId = id
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.sprite: Sprite = sprite
        self.direction: Direction = direction
        self._speed: int = speed
        self._speed_multiplier: int = 1
        self._effective_speed: int = speed
        self._is_moving = True
        self.pygame_collision_rect: Rect = Rect(self.x, self.y, size[0], size[1])
        self.movement_animation_progress: float = 0
        self.visible: bool = True
        self.view_z: int = 0
        self.movement_changed: Observable = None
        self.position_changed: Observable = None
        #self.is_moving = is_moving # optional
        #self.is_thinking = is_thinking # optional
        #self.is_speaking = is_speaking # optional


    def check_collision(self, otherRect: Rect):
        self.pygame_collision_rect.colliderect(otherRect)
    
    def rect(self):
        return self.x, self.y, 0, 0

    def get_position(self):
        return self.x, self.y
