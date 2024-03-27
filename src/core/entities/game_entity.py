from typing import Tuple

from pygame.rect import Rect

from src.core.common import *

class WorldEntity:
    def __init__(self, id:int, pos: Tuple[int, int], size: Tuple[int, int], sprite: Sprite, direction: Direction = Direction.LEFT, speed: int = 0):
        self.id: int = id
        self.x: int = pos[0]
        self.y: int = pos[1]
        self.sprite: Sprite = sprite
        self.direction: Direction = direction
        self._speed: int = speed
        self._speed_multiplier: int = 1
        self._effective_speed: int = speed
        self.pygame_collision_rect: Rect = Rect(self.x, self.y, size[0], size[1])
        self.movement_animation_progress: float = 0
        self.visible: bool = True
        self.view_z: int = 0
        self.movement_changed: Observable = None
        self.position_changed: Observable = None

        self._is_moving = True # ToDo handle states proberly

    def set_moving_in_dir(self, direction: Direction):
        if direction is None:
            raise Exception("Need to provide a valid direciton to move in")
        self.direction = direction
        if not self._is_moving:
            self.notify_movement_observers(True)
        self._is_moving = True

    def set_not_moving(self):
        if self._is_moving:
            self.notify_movement_observers(False)
        self._is_moving = False

    def notify_movement_observers(self, is_moving: bool):
        #if self.movement_changed is not None:
        #    self.movement_changed.notify(is_moving)
        pass

    def update_movement_animation(self, time_passed: Millis):
        if self._is_moving:
            self.update_animation(time_passed)

    def update_animation(self, time_passed):
        self.movement_animation_progress = (self.movement_animation_progress + float(time_passed) / 700) % 1


    def check_collision(self, otherRect: Rect):
        self.pygame_collision_rect.colliderect(otherRect)
    
    def rect(self):
        return self.x, self.y, 0, 0

    def get_position(self):
        return self.x, self.y
    
    def set_position(self, new_position: Tuple[int, int]):
        self.x = new_position[0]
        self.y = new_position[1]
        self.pygame_collision_rect.x = self.x
        self.pygame_collision_rect.y = self.y
        #self.notify_position_observers()
    
    def rotate_right(self):
        dirs = {
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN
        }
        self.direction = dirs[self.direction]

    def rotate_left(self):
        dirs = {
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN
        }
        self.direction = dirs[self.direction]
