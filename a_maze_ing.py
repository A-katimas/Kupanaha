from parthing import parth
from utils import color, info, a_maze, clear
from maze.maker import make_a_maze
from utils.player import Player
import sys

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
    clear()
    player = Player((20, 50))
    info(config, (2, 2))

    a_maze(make_a_maze())
    player.move()

if __name__ == "__main__":
    if folders_exist:
        main()
