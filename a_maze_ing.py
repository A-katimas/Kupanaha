from parthing import parth
from utils import (
    color,
    clear,
    cursor,
    cursor_more_line,
    move_cursor_to_bottom,
    Presentation,
)
from maze import Maze
from utils.player import Player
from utils.cursor import cursor_hide

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

    player = Player([config.Entry[0], config.Entry[1]], "🦦")
    press = Presentation(config, player)

    press.loop()
    # player.print_self()

    # move_cursor_to_bottom()


if __name__ == "__main__":
    if folders_exist:
        main()
