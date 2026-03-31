from utils.wall import *
from utils import cursor_more_line
import random


THEMES = {
    "white": [[245, 245, 245], [80, 80, 80]],
    "pink": [[255, 200, 220], [180, 40, 100]],
    "blue": [[200, 220, 255], [30, 70, 180]],
    "green": [[200, 240, 210], [30, 120, 60]],
    "red": [[255, 200, 200], [180, 30, 30]],
    "yellow": [[255, 250, 200], [180, 140, 20]],
    "purple": [[230, 200, 255], [100, 30, 180]],
    "orange": [[255, 225, 190], [200, 90, 20]],
    "cyan": [[190, 245, 255], [20, 150, 180]],
    "dark": [[30, 30, 30], [200, 200, 200]],
    "cyberpunk": [[20, 10, 40], [255, 0, 200]],
    "forest": [[210, 240, 200], [40, 80, 30]],
    "ocean": [[190, 220, 240], [20, 60, 120]],
    "lava": [[40, 10, 10], [255, 80, 20]],
    "gold": [[255, 240, 180], [180, 130, 20]],
    "ice": [[220, 240, 255], [100, 180, 220]],
    "midnight": [[10, 10, 40], [80, 80, 200]],
    "sakura": [[255, 220, 230], [200, 80, 120]],
    "matrix": [[10, 20, 10], [0, 200, 50]],
    "sunset": [[255, 200, 170], [200, 60, 20]],
}

class Maze:
    def __init__(self, size, Enter, Exit, start_print, theme):
        self.size = size
        self.enter = Enter
        self.exit = Exit
        self.start_print = start_print
        self.maze = self.make_a_maze()
        self.print_maze = self.make_a_print_maze()
        self.backcolor = []
        self.wallcolor = []
        self.change_theme(theme)

    def get_theme(self) -> tuple:
        return tuple(self.backcolor), tuple(self.wallcolor)

    def change_theme(self, new_theme: str) -> None:
        if new_theme not in THEMES:
            raise ValueError(f"Thème inconnu : {new_theme}")
        self.backcolor = THEMES[new_theme][0]
        self.wallcolor = THEMES[new_theme][1]

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

                y = self.start_print[1] + col_index * 6
                x = self.start_print[0] + row_index * 3

                tile_class = tile_map.get(cell)

                if tile_class:
                    result.append(tile_class((x, y)))
                else:
                    print(f"Valeur inconnue: {cell}")

        return result

    def make_a_maze(self) -> list:
        from parthing import parth_maze

        self.maze = generate_maze(self.size[0], self.size[1])
        parth_maze(self)
        return self.maze


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
