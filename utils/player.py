from .cursor import cursor
from maze.maker import Maze


class Player:
    def __init__(self, pos: tuple, sprite: str) -> None:
        self.pos = pos
        self.sprite = sprite

    def move(self):
        print(cursor(self.pos, self.sprite))
