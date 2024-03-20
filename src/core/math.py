
from typing import List, Tuple

from src.core.common import Direction


def sum_of_vectors(v1: Tuple[int, int], v2: Tuple[int, int]) -> Tuple[int, int]:
    return v1[0] + v2[0], v1[1] + v2[1]

def is_x_and_y_within_distance(a: Tuple[int, int], b: Tuple[int, int], distance: int):
    return abs(a[0] - b[0]) < distance and abs(a[1] - b[1]) < distance

def get_manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_directions_to_position(from_entity, position) -> Tuple[Direction, Direction]:
    dx = position[0] - from_entity.x
    dy = position[1] - from_entity.y
    dir_from_dx = lambda dx: Direction.RIGHT if dx > 0 else (Direction.LEFT if dx < 0 else None)
    dir_from_dy = lambda dy: Direction.UP if dy < 0 else (Direction.DOWN if dy > 0 else None)
    if abs(dx) > abs(dy):
        return dir_from_dx(dx), dir_from_dy(dy)
    else:
        return dir_from_dy(dy), dir_from_dx(dx)
    

def get_perpendicular_directions(direction: Direction) -> List[Direction]:
    if direction == direction.LEFT or direction == direction.RIGHT:
        return [Direction.UP, Direction.DOWN]
    else:
        return [Direction.LEFT, Direction.RIGHT]


def get_opposite_direction(direction: Direction) -> Direction:
    if direction == direction.LEFT:
        return direction.RIGHT
    if direction == direction.RIGHT:
        return direction.LEFT
    if direction == direction.UP:
        return direction.DOWN
    if direction == direction.DOWN:
        return direction.UP


def get_position_from_center_position(center_position: Tuple[int, int], size: Tuple[int, int]):
    return center_position[0] - size[0] / 2, center_position[1] - size[1] / 2


def translate_in_direction(position: Tuple[int, int], direction: Direction, amount: int) -> Tuple[int, int]:
    if direction == Direction.RIGHT:
        return position[0] + amount, position[1]
    elif direction == Direction.DOWN:
        return position[0], position[1] + amount
    elif direction == Direction.LEFT:
        return position[0] - amount, position[1]
    elif direction == Direction.UP:
        return position[0], position[1] - amount
    else:
        raise Exception("Unhandled direction: " + str(direction))