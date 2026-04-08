from parthing import parth
from utils import (
    color,
    clear,
    Presentation,
)
from maze import Maze
from utils.player import Player
from utils.cursor import cursor_hide
import random

import sys


folders_exist = True
try:
    open("config.txt", "r")

except FileNotFoundError as e:
    print(e)
    folders_exist = False


def main():
    if len(sys.argv) < 2:
        print(
            color(
                f"Usage: python3 {sys.argv[0]} <item1:qty> <item2:qty> ...",
                255,
                200,
                200,
            )
        )
        sys.exit(1)
    config = parth(sys.argv[1])
    if config == None:
        return 0

    clear()
    random.seed(config.SEED)
    player = Player([config.ENTRY[0], config.ENTRY[1]], "🦦")
    press = Presentation(config, player)

    press.loop()
    # player.print_self()

    # move_cursor_to_bottom()


if __name__ == "__main__":
    if folders_exist:
        main()
