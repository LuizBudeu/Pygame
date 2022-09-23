from .common.settings import *
from .common.ui_utils import *
from .common.entity import Entity


class Wall(Entity):
    def __init__(self, x, y, width, height, color, name="wall", immortal=True):
        super().__init__(x, y, width, height, color, name=name, immortal=immortal)
