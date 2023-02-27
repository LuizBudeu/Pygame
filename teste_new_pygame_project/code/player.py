from .framework.observer import Observer
from enum import Enum


class Player(Observer):
    class Actions(Enum):
        MOVE_UP = 1
        MOVE_DOWN = 2
        MOVE_LEFT = 3
        MOVE_RIGHT = 4
        SHOOT = 5
    
    def __init__(self):
        pass
        
    def on_notify(self, action):
        print(action)
