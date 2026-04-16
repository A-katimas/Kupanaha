from utils.draw import Wall, cursor, color
from utils import cursor


class PathDrawer():
    def __init__(self, path: list[tuple[int, int]]):
        self.path = path

    def path_draw(self, offset_line: int = 0, offset_col: int = 0) -> None:
        dot = color("•", 255, 0, 0)
        for pos in self.path:
            actual_pos = (pos[0] + offset_line, pos[1] + offset_col)
            print(cursor(actual_pos, dot), end="", flush=True)

