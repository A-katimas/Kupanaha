from parthing import parth
from utils import (
    color,
    info,
    a_maze,
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
    amazeing = Maze(
        (config.Width, config.Height),
        config.Entry,
        config.Exit,
        (15, 15),
        "white",
    )
    clear()

    player = Player([amazeing.enter[0], amazeing.enter[1]], "🦦")
    press = Presentation(config, amazeing, player)
    # info(config, (2, 2))
    a_maze(
        amazeing.printable_maze,
        amazeing.get_theme()[0],
        amazeing.get_theme()[1],
    )
    move_cursor_to_bottom()

    # while player.move() != "a":
    # cursor_more_line((1,1),amazeing.maze)
    # while player.move() != "a":
    a_maze(
        amazeing.printable_maze,
        amazeing.get_theme()[0],
        amazeing.get_theme()[1],
    )
    press.start()
    # press.loop()
    # player.print_self()

    move_cursor_to_bottom()


if __name__ == "__main__":
    if folders_exist:
        main()
