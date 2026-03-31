from utils.wall import *
from utils import cursor_more_line
import random


class Maze:
    def __init__(self, size: tuple, Enter: tuple, Exit: tuple, start_print: tuple):
        self.size = size
        self.enter = Enter
        self.exit = Exit
        self.start_print = start_print
        self.maze = self.make_a_maze()
        self.print_maze = self.make_a_print_maze()

    def make_a_print_maze(self) -> list:
        result = []

        tile_map = {
            "0": Nothing,
            "1": N,
            "2": E,
            "3": S_W,
            "4": S,
            "5": N_E,
            "6": N_W,
            "7": S_E,
            "8": W,
            "9": S_N,
            "A": E_W,
            "B": N_S_E,
            "C": S_E_W,
            "D": N_E_W,
            "E": N_S_E_W,
        }

        for row_index, row in enumerate(self.maze):
            for col_index, cell in enumerate(row):

                y = self.start_print[1] + col_index * 6  # largeur d'une tile
                x = self.start_print[0] + row_index * 3  # hauteur d'une tile

                tile_class = tile_map.get(cell)

                if tile_class:
                    result.append(tile_class((x, y)))
                else:
                    print(f"Valeur inconnue: {cell}")

        return result

    def make_a_maze(self) -> list:
        from parthing import parth_maze

        self.maze = generate_maze(self.size[0], self.size[1])
        parth_maze(self)  # travaille sur list[list[str]]

        # Aplatit seulement maintenant
        return self.maze


# Dans maker.py - renomme les constantes
DIR_N, DIR_E, DIR_S, DIR_W = 0x1, 0x2, 0x4, 0x8
OPPOSITE = {DIR_N: DIR_S, DIR_S: DIR_N, DIR_E: DIR_W, DIR_W: DIR_E}
DELTA = {DIR_N: (0, -1), DIR_E: (1, 0), DIR_S: (0, 1), DIR_W: (-1, 0)}

def generate_maze(width: int, height: int) -> list:
    maze = [[0] * width for _ in range(height)]
    visited = [[False] * width for _ in range(height)]

    def carve(x, y):
        visited[y][x] = True
        directions = [DIR_N, DIR_E, DIR_S, DIR_W]
        random.shuffle(directions)

        for direction in directions:
            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                maze[y][x] |= direction
                maze[ny][nx] |= OPPOSITE[direction]
                carve(nx, ny)

    carve(0, 0)

    return [[hex(cell)[2:].upper() for cell in row] for row in maze]