from parthing import parth
from utils import color, info, a_maze, clear, cursor, cursor_more_line
from maze import Maze
from utils.player import Player
from utils.cursor import move_cursor_to_bottom
import sys
import os

folders_exist = True
try:
    open("config.txt", "r")

except FileExistsError as e:
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
    amazeing = Maze((config.Width, config.Height), config.Entry, config.Exit, (10, 10))
    clear()
    size = os.get_terminal_size()
    player = Player((11, 30), "🦦")
    info(config, (2, 2))

    # cursor_more_line((1,1),amazeing.maze)
    a_maze(amazeing.print_maze)
    player.move()
    print(size.lines - 10, size.columns - 10)
    move_cursor_to_bottom()


if __name__ == "__main__":
    if folders_exist:
        main()
