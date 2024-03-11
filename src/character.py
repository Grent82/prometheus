class Character:
    x_pos: int
    y_pos: int
    orientation: int
    is_moving: bool
    is_thinking: bool
    is_speaking: bool
    speed: float


    def __init__(self, x_pos:int, y_pos:int, orientation:int, is_moving:bool = False, is_thinking:bool = False, is_speaking:bool = False):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.orientation = orientation
        self.is_moving = is_moving
        self.is_thinking = is_thinking
        self.is_speaking = is_speaking

