import utils.wall as wall
from utils import draw_a_maze
import random
from enum import Enum
from typing import Callable, Any

THEMES = {
    "white": [[245, 245, 245], [80, 80, 80]],
    "pink": [[255, 0, 250], [155, 0, 155]],
    "blue": [[50, 50, 255], [50, 50, 150]],
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
    "neon": [[5, 5, 5], [255, 255, 0]],
    "blood": [[10, 0, 0], [180, 0, 0]],
    "toxic": [[10, 20, 5], [50, 255, 0]],
    "sand": [[255, 240, 200], [180, 140, 80]],
    "ash": [[50, 50, 50], [150, 150, 150]],
    "copper": [[40, 20, 10], [180, 100, 40]],
    "arctic": [[240, 250, 255], [150, 210, 240]],
    "volcano": [[20, 5, 0], [255, 60, 0]],
    "jade": [[10, 30, 20], [50, 180, 100]],
    "rose": [[255, 230, 235], [220, 80, 100]],
    "steel": [[20, 25, 30], [100, 130, 160]],
    "amber": [[30, 15, 0], [255, 150, 0]],
    "void": [[0, 0, 0], [80, 0, 180]],
    "ghost": [[240, 240, 255], [180, 180, 220]],
    "rust": [[30, 10, 5], [180, 70, 30]],
    "teal": [[10, 30, 30], [0, 180, 160]],
    "lavender": [[240, 235, 255], [130, 100, 200]],
    "toxic_green": [[0, 15, 0], [0, 255, 80]],
    "deep_sea": [[0, 10, 30], [0, 80, 160]],
    "inferno": [[15, 0, 0], [255, 100, 0]],
    "snow": [[255, 255, 255], [200, 220, 255]],
    "poison": [[20, 0, 30], [180, 0, 255]],
    "bronze": [[20, 10, 0], [140, 80, 20]],
    "aurora": [[5, 15, 20], [0, 255, 180]],
    "crimson": [[20, 0, 5], [200, 0, 50]],
}


def add_pos(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def abs_dist(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Direction(Enum):
    DIR_S = 0x4
    DIR_N = 0x1
    DIR_E = 0x2
    DIR_W = 0x8

    def oppo(self) -> "Direction":
        return {
            Direction.DIR_N: Direction.DIR_S,
            Direction.DIR_S: Direction.DIR_N,
            Direction.DIR_E: Direction.DIR_W,
            Direction.DIR_W: Direction.DIR_E,
        }[self]

    def delta(self) -> tuple[int, int]:
        return {
            Direction.DIR_N: (0, -1),
            Direction.DIR_E: (1, 0),
            Direction.DIR_S: (0, 1),
            Direction.DIR_W: (-1, 0),
        }[self]


class Maze:
    def __init__(
        self,
        size: tuple[int, int],
        Enter: tuple[int, int],
        Exit: tuple[int, int],
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
        self.maze: list[Any] = self.make_a_maze()
        self.folders = folders

    def get_tuple_theme(
        self,
    ) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        back = (self.backcolor[0], self.backcolor[1], self.backcolor[2])
        wall = (self.wallcolor[0], self.wallcolor[1], self.wallcolor[2])
        return (back, wall)

    def get_theme_name(self) -> str:
        for name, colors in THEMES.items():
            if colors[0] == self.backcolor and colors[1] == self.wallcolor:
                return name
        return "white"

    def change_theme(self, new_theme: str) -> None:
        if new_theme not in THEMES:
            raise ValueError(f"Thème inconnu : {new_theme}")
        self.backcolor = THEMES[new_theme][0]
        self.wallcolor = THEMES[new_theme][1]

    def update_printable_maze(self) -> None:
        result = []
        tile_map: dict[int, Callable[[tuple[int, int]], wall.Wall]] = {
            15: wall.Nothing,
            14: wall.N,
            13: wall.E,
            12: wall.N_E,
            11: wall.S,
            10: wall.N_S,
            9: wall.E_S,
            8: wall.N_E_S,
            7: wall.W,
            6: wall.N_W,
            5: wall.E_W,
            4: wall.N_E_W,
            3: wall.S_W,
            2: wall.N_S_W,
            1: wall.E_S_W,
            0: wall.N_E_S_W,
            16: wall.petit_logo42,
            17: wall.gros_logo42_0,
            18: wall.gros_logo42_1,
            19: wall.gros_logo42_2,
            20: wall.gros_logo42_3,
            21: wall.gros_logo42_4,
            22: wall.gros_logo42_5,
            23: wall.gros_logo42_6,
            24: wall.gros_logo42_7,
            25: wall.gros_logo42_3,
            26: wall.gros_logo42_4,
            27: wall.gros_logo42_1,
            28: wall.gros_logo42_8,
            29: wall.gros_logo42_3,
            30: wall.gros_logo42_9,
            31: wall.gros_logo42_1,
            32: wall.gros_logo42_2,
            33: wall.gros_logo42_3,
            34: wall.gros_logo42_10,
        }

        for col_index, col in enumerate(self.maze):
            for row_index, cell in enumerate(col):

                x = self.start_print[0] + row_index * 3
                y = self.start_print[1] + col_index * 6

                tile_class = tile_map.get(cell)

                if tile_class:
                    res = tile_class((x, y))
                    if self.enter == (col_index, row_index):
                        res.entre = True
                    if self.exit == (col_index, row_index):
                        res.exit = True
                    result.append(res)

                else:
                    result.append(wall.petit_logo42((x, y)))
        self.printable_maze = result

    def make_a_maze(self) -> list[str]:
        self.maze = self.generate_maze()
        return self.maze

    def generate_maze(self) -> list[str]:
        width, height = self.size[0], self.size[1]
        self.maze = [[15] * height for _ in range(width)]
        self.logo42()
        # self.update_printable_maze()
        return self.maze

    def backtrack(self) -> None:
        stack = [(0, 0)]
        while stack:
            self.update_printable_maze()
            draw_a_maze(
                self.printable_maze,
                self.get_tuple_theme()[0],
                self.get_tuple_theme()[1],
            )
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
                == 15
            ]
            if dir_possible:
                goal = random.choice(dir_possible)
                self.maze[current[0]][current[1]] &= ~goal.value
                next_pos = add_pos(current, goal.delta())
                self.maze[next_pos[0]][next_pos[1]] &= ~goal.oppo().value
                stack.append(next_pos)
            else:
                stack.pop()

    def prims(self) -> None:
        start = (0, 0)
        queue = [(0, 0)]
        while queue:
            self.update_printable_maze()
            draw_a_maze(
                self.printable_maze,
                self.get_tuple_theme()[0],
                self.get_tuple_theme()[1],
            )
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
                == 15
            ]
            if dir_possible:
                for goal in dir_possible:
                    # goal = random.choice(dir_possible)
                    self.maze[current[0]][current[1]] &= ~goal.value
                    next_pos = add_pos(current, goal.delta())
                    self.maze[next_pos[0]][next_pos[1]] &= ~goal.oppo().value
                    queue.append(next_pos)
            else:
                queue.remove(current)

    def draw_in_folders(self) -> None:
        with open(self.folders, "w") as fd:
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if self.maze[x][y] > 15:
                        print("F", end="", file=fd)
                    else:
                        cell = hex(self.maze[x][y])[2:].upper()
                        print(cell, end="", file=fd)
                print(file=fd)
            print(file=fd)
            print(f"{self.enter[0]},{self.enter[1]}", file=fd)
            print(f"{self.exit[0]},{self.exit[1]}", file=fd)

    def make_it_false(self) -> None:
        break_wall = random.randint(len(self.maze), len(self.maze) * 2)

        while break_wall != 0:
            self.update_printable_maze()
            draw_a_maze(
                self.printable_maze,
                self.get_tuple_theme()[0],
                self.get_tuple_theme()[1],
            )
            rand_x = random.randint(0, self.size[0] - 1)
            rand_y = random.randint(0, self.size[1] - 1)
            current = (rand_x, rand_y)

            dir_possible = [
                direct
                for direct in Direction
                if 0 <= add_pos(current, direct.delta())[0] < self.size[0]
                and 0 <= add_pos(current, direct.delta())[1] < self.size[1]
            ]
            if not dir_possible:
                continue
            goal = random.choice(dir_possible)

            if self.maze[current[0]][current[1]] > 15:
                continue
            next_pos = add_pos(current, goal.delta())
            if self.maze[next_pos[0]][next_pos[1]] > 15:
                continue

            self.maze[current[0]][current[1]] &= ~goal.value
            self.maze[next_pos[0]][next_pos[1]] &= ~goal.oppo().value

            break_wall -= 1

    def logo42(self) -> None:
        if self.size[0] < 11 and self.size[1] < 12:
            pos42 = (self.size[0] // 2, self.size[1] // 2)
            if (pos42 == self.enter) or (pos42 == self.exit):
                self.maze[pos42[0] + 1][pos42[1]] = 16
            else:
                self.maze[pos42[0]][pos42[1]] = 16
        else:
            grand_logo = [
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 2),
                (2, 2),
                (2, 3),
                (2, 4),
                (4, 0),
                (5, 0),
                (6, 0),
                (6, 1),
                (6, 2),
                (5, 2),
                (4, 2),
                (4, 3),
                (4, 4),
                (5, 4),
                (6, 4),
            ]
            pos42 = ((self.size[0] // 2) - 3, (self.size[1] // 2) - 2)

            pos_grand_logo = list(
                (x + pos42[0], y + pos42[1]) for x, y in grand_logo
            )
            if not any(
                map(lambda x: x in (self.enter, self.exit), pos_grand_logo)
            ):
                j = 1
                for i in grand_logo:
                    self.maze[pos42[0] + i[0]][pos42[1] + i[1]] = j + 16
                    j += 1
            else:
                pos42 = (self.size[0] // 2, self.size[1] // 2)
                if (pos42 == self.enter) or (pos42 == self.exit):
                    self.maze[pos42[0] + 1][pos42[1]] = 16
                else:
                    self.maze[pos42[0]][pos42[1]] = 16
