from typing import Dict

from src.core.common import Direction, Sprite
from src.core.views.image_loading import Animation

ENTITY_SPRITE_INITIALIZERS: Dict[Sprite, Dict[Direction, Animation]] = {}