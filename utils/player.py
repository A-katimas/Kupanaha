from .cursor import cursor
from maze.maker import Maze
import sys
import tty
import termios


class Player:
    def __init__(self, pos: list, sprite: str) -> None:
        self.pos = pos
        self.sprite = sprite

    def move(self) -> str:
        get_move = get_key()
        match (get_move):
            case "z":
                self.pos[0] -= 1
            case "s":
                self.pos[0] += 1
            case "q":
                self.pos[1] -= 2
            case "d":
                self.pos[1] += 2
        return get_move

    def print_self(self):
        print(cursor(tuple(self.pos), self.sprite))


def get_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        # Touches spéciales (flèches etc.) envoient 3 caractères
        if key == "\x1b":
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key
