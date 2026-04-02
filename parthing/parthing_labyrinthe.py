from typing import TYPE_CHECKING
from maze import Maze

# tile_map = {
#    "1": N,
#    "2": E,
#    "3": S_W,
#    "4": S,
#    "5": N_E,
#    "6": N_W,
#    "7": S_E,
#    "8": W,
#    "9": S_N,
#    "A": E_W,
#    "B": N_S_E,
#    "C": S_E_W,
#    "D": N_E_W,
#    "E": N_E_W,
# }

DIR_N, DIR_E, DIR_S, DIR_W = 0x1, 0x2, 0x4, 0x8


def fix_border_tiles(maze):
    height = len(maze.maze)
    width = len(maze.maze[0])

    for y, row in enumerate(maze.maze):
        for x, cell in enumerate(row):
            bits = int(cell, 16)

            if x == 0:
                bits &= ~DIR_W.value
            if x == width - 1:
                bits &= ~DIR_E.value
            if y == 0:
                bits &= ~DIR_N.value
            if y == height - 1:
                bits &= ~DIR_S.value

            maze.maze[y][x] = hex(bits)[2:].upper()


def parth_maze(maze: Maze):
    fix_border_tiles(maze)
