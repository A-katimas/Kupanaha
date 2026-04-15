from maze.maker import Direction

# from utils.wall as wall
from parthing import BaseConfig
from utils.color import bg_color
from utils.cursor import cursor
from typing import Any


class Solver:
    def __init__(self, maze: list[Any], config: BaseConfig):
        self.maze = maze
        self.config = config

    def solve_maze(self):
        queue = [self.config.enter]
        visited = {self.config.enter}
        came_from = {}

        while queue:
            current = queue
            x, y = current

            for dir in Direction:
                dx, dy = dir.delta()
                nx = x + dx
                ny = y + dy
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    if self.maze[x][y] == 0:  # utiliser wall et pas le binaire
                        came_from[(nx, ny)] = (x, y)
                else:
                    print(cursor((x, y), bg_color("  ", 30, 30, 30)))
