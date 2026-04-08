from utils.wall import *
from utils import cursor_more_line, draw_a_maze
import random
from enum import Enum
from time import sleep

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


def abs_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Direction(Enum):
    DIR_S = 0x4
    DIR_N = 0x1
    DIR_E = 0x2
    DIR_W = 0x8

    def oppo(self):
        return {
            Direction.DIR_N: Direction.DIR_S,
            Direction.DIR_S: Direction.DIR_N,
            Direction.DIR_E: Direction.DIR_W,
            Direction.DIR_W: Direction.DIR_E,
        }[self]

    def delta(self):
        return {
            Direction.DIR_N: (0, -1),
            Direction.DIR_E: (1, 0),
            Direction.DIR_S: (0, 1),
            Direction.DIR_W: (-1, 0),
        }[self]


def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


class Maze:
    def __init__(
        self,
        size: tuple,
        Enter: tuple,
        Exit: tuple,
        start_print: list[int],
        theme: str,
        folders: str,
    ):
        self.size = size
        self.enter = Enter
        self.exit = Exit
        self.backcolor = [50, 50, 50]
        self.wallcolor = [255, 255, 255]
        self.change_theme(theme)
        self.start_print = start_print
        self.maze: list = self.make_a_maze()
        self.folders = folders

    def get_theme(self) -> tuple:
        return tuple(self.backcolor), tuple(self.wallcolor)

    def change_theme(self, new_theme: str) -> None:
        if new_theme not in THEMES:
            raise ValueError(f"Thème inconnu : {new_theme}")
        self.backcolor = THEMES[new_theme][0]
        self.wallcolor = THEMES[new_theme][1]

    def update_printable_maze(self) -> None:
        result = []

        tile_map = {
            0: Nothing,
            1: N,
            2: E,
            3: N_E,
            4: S,
            5: N_S,
            6: E_S,
            7: N_E_S,
            8: W,
            9: N_W,
            10: E_W,
            11: N_E_W,
            12: S_W,
            13: N_S_W,
            14: E_S_W,
            15: N_E_S_W,
        }

        for col_index, col in enumerate(self.maze):
            with open("test/backtr", "r+") as f:
                for row_index, cell in enumerate(col):

                    x = self.start_print[0] + row_index * 3
                    y = self.start_print[1] + col_index * 6

                    tile_class = tile_map.get(cell)

                    if tile_class:
                        res = tile_class((x, y))
                        print(x, y, file=f)
                        if self.enter == (col_index, row_index):
                            res.entre = True
                        if self.exit == (col_index, row_index):
                            res.exit = True
                        result.append(res)

                    else:
                        print(f"Valeur inconnue: {cell}")
        self.printable_maze = result

    def make_a_maze(self) -> list:
        self.maze = self.generate_maze()
        return self.maze

    def generate_maze(self) -> list:
        width, height = self.size[0], self.size[1]
        self.maze = [[0] * height for _ in range(width)]
        self.update_printable_maze()
        return self.maze

    def backtrack(self) -> None:
        stack = [(0, 0)]
        while stack:
            self.update_printable_maze()
            draw_a_maze(
                self.printable_maze, self.get_theme()[0], self.get_theme()[1]
            )
            sleep(0.001)
            current = stack[-1]
            dir_possible = [
                direct
                for direct in Direction
                if 0 <= add_pos(current, direct.delta())[0] < self.size[0]
                and 0 <= add_pos(current, direct.delta())[1] < self.size[1]
            ]
            dir_possible = [
                direct
                for direct in dir_possible
                if self.maze[add_pos(current, direct.delta())[0]][
                    add_pos(current, direct.delta())[1]
                ]
                == 0
            ]
            if dir_possible:
                goal = random.choice(dir_possible)
                self.maze[current[0]][current[1]] += goal.value
                next_pos = add_pos(current, goal.delta())
                self.maze[next_pos[0]][next_pos[1]] += goal.oppo().value
                stack.append(next_pos)
            else:
                stack.pop()

    def prims(self) -> None:
        start = (0, 0)
        queue = [(0, 0)]
        while queue:
            self.update_printable_maze()
            draw_a_maze(
                self.printable_maze, self.get_theme()[0], self.get_theme()[1]
            )
            sleep(0.005)
            weight = [1] if start in queue else []
            weight.extend(
                [abs_dist(start, pos) for pos in queue if pos != start]
            )
            # a = max(weight)
            # weight = [a - b + 1 for b in weight]
            weight = [b**2 for b in weight]
            current = random.choices(population=queue, weights=weight)[0]
            dir_possible = [
                direct
                for direct in Direction
                if 0 <= add_pos(current, direct.delta())[0] < self.size[0]
                and 0 <= add_pos(current, direct.delta())[1] < self.size[1]
            ]
            dir_possible = [
                direct
                for direct in dir_possible
                if self.maze[add_pos(current, direct.delta())[0]][
                    add_pos(current, direct.delta())[1]
                ]
                == 0
            ]

            if dir_possible:
                for goal in dir_possible:
                    # goal = random.choice(dir_possible)
                    self.maze[current[0]][current[1]] += goal.value
                    next_pos = add_pos(current, goal.delta())
                    self.maze[next_pos[0]][next_pos[1]] += goal.oppo().value
                    queue.append(next_pos)
            else:
                queue.remove(current)
        # self.draw_in_folders()

    def draw_in_folders(self):
        with open(self.folders, "r+") as fd:
            for i in self.maze:
                print(i, file=fd)
