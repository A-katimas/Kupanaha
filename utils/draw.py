from typing import TYPE_CHECKING
from .wall import *
from .color import color
from .cursor import get_key, clear

# from .player import get_key
from .cursor import cursor_more_line, cursor

import os

if TYPE_CHECKING:
    from utils import Player
    from parthing import BaseConfig


class Presentation:
    def __init__(self, config: "BaseConfig", player: "Player"):
        from maze.maker import Maze

        self.scren_size = os.get_terminal_size()
        self.config = config
        self.player = player
        self.info_block = InfoBlock(config, (15, 50))
        self.maze = Maze(
            (config.Width, config.Height),
            config.Entry,
            config.Exit,
            [12, 35],
            "white",
        )
        self.logo = [
            otter((1, 1)),
            amazing((1, 40)),
            red_panda((1, self.scren_size.columns - 45)),
        ]
        self.start()

    def start(self):

        lines = self.maze.size[0] + 20
        columns = self.maze.size[1] * 6 + 45

        def good_size(line: int, columns: int) -> list[str]:
            print("je suis la ")
            if line >= self.scren_size.lines:
                str_line = color(f"{line}", 255, 0, 0)
            else:
                str_line = color(f"{line}", 0, 255, 0)
            if columns >= self.scren_size.columns:
                str_columns = color(f"{columns}", 255, 0, 0)
            else:
                str_columns = color(f"{columns}", 0, 255, 0)
            return [str_line, str_columns]

        print(cursor((25, 50), "touch any key to see your screen"))
        print(self.info_block.wall())
        have = good_size(lines, columns)
        print(cursor((13, 50), f"you do have {have[0]} : x   {have[1]} : y"))
        for e in self.logo:
            print(e.wall())
        while (
            get_key() != "\r"
            or self.scren_size.lines <= lines
            and self.scren_size.columns <= columns
        ):
            self.scren_size = os.get_terminal_size()
            clear()
            print(cursor((25, 50), "touch any key to see your screen"))
            print(self.info_block.wall())
            have = good_size(lines, columns)
            print(
                cursor((13, 50), f"you do have {have[0]} : x   {have[1]} : y")
            )
            self.logo[2].pos = ((1), (self.scren_size.columns - 45))
            for e in self.logo:
                print(e.wall())

    def loop(self):
        self.info_block.pos = ((self.scren_size.lines - 15), (1))
        print(self.info_block.wall())
        self.maze.backtrack()

    def pressentation_enter():
        pass


class InfoBlock(Wall):
    WIDTH = 32

    def __init__(self, config: "BaseConfig", pos: tuple):
        super().__init__(pos)
        self.config = config

    def wall(self) -> str:
        size = os.get_terminal_size()
        w = self.WIDTH

        border_top = "█" + "▀" * w + "█"
        border_bottom = "█" + "▄" * w + "█"

        # ██ ▄▄ ▀▀
        def line(content: str) -> str:
            import re

            clean = re.sub(r"\x1b\[[0-9;]*m", "", content)
            padding = w - len(clean) - 2
            return "█ " + content + " " * padding + " █"

        c = self.config
        screen = f"x : {size.lines - 10}, y : {size.columns - 10}"

        lines = [
            border_top,
            line(f"         CONFIG"),
            line(f"      WIDTH = {color(c.Width,       150, 100, 200)}"),
            line(f"     HEIGHT = {color(c.Height,      140, 110, 190)}"),
            line(
                f"      ENTRY = x : {color(c.Entry[0], 130, 120, 180)} y : {color(c.Entry[1], 130, 120, 180)}"
            ),
            line(
                f"       EXIT = x : {color(c.Exit[0],  120, 130, 170)} y : {color(c.Exit[1],  120, 130, 170)}"
            ),
            line(f"OUTPUT_FILE = {color(c.Output_file, 110, 140, 160)}"),
            line(f"    PERFECT = {color(c.Perfect,     100, 150, 150)}"),
            line(f"screen size = {color(screen,         90, 160, 140)}"),
            border_bottom,
        ]

        return cursor_more_line(self.pos, lines)


def draw_a_maze(maze: list[Wall], backcolor: tuple, wallcolor: tuple):
    r = 0
    g = 0
    b = 0
    for i in maze:
        print(
            bg_color(
                color(i.wall(), backcolor[r], backcolor[g], backcolor[b]),
                wallcolor[r],
                wallcolor[g],
                wallcolor[b],
            ),
            end="",
        )


# def debug_key():
#     import tty, termios, sys

#     fd = sys.stdin.fileno()
#     old = termios.tcgetattr(fd)
#     try:
#         tty.setraw(fd)
#         key = sys.stdin.read(1)
#         if key == "\x1b":
#             key += sys.stdin.read(2)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old)
#     print(f"raw: {repr(key)}")


class otter(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "        ⢀⣀⡤⠴⠶⠶⠒⠲⠦⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀   ",
                "⠀⠀⠀⠀⢀⡠⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠲⠤⣄⡀⠀⠀⠀⠀⠀",
                "⠀⠀⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡿⠀⠀⠀⠀⠀",
                "⠀⢾⣅⡀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⢀⡦⠤⠄⠀⠀⢻⡀⠀⠀⠀⠀⠀",
                "⠀⠈⢹⡏⠀⠀⠐⠋⠉⠁⠀⠻⢿⠟⠁⠀⠀⢤⠀⠀⠠⠤⢷⣤⣤⢤⡄⠀",
                "⠀⠀⣼⡤⠤⠀⠀⠘⣆⡀⠀⣀⡼⠦⣄⣀⡤⠊⠀⠀⠀⠤⣼⠟⠀⠀⢹⡂",
                "⠀⠊⣿⡠⠆⠀⠀⠀⠈⠉⠉⠙⠤⠤⠋⠀⠀⠀⠀⠀⠀⡰⠋⠀⠀⠀⡼⠁",
                "⠀⢀⡾⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⠁⠀⠀⠀⣸⠁⠀",
                "⠀⠀⠀⡼⠙⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀",
                "⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀",
                "⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀",
                "⣾⠁⠀⢀⣠⡴⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀",
                "⠈⠛⠻⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀",
            ],
        )


class red_panda(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        panda = cursor_more_line(
            self.pos,
            [
                "    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠊⡁⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⢠⠁⠀⢫⡑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠐⠑⠆⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢸⠀⢷⠀⠳⣄⠏⠢⣀⡀⢀⠀⠀⠀⢀⠴⠂⢩⠏⢀⡔⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢇⠈⣇⠼⣇⠀⢹⠟⠁⠁⠈⠉⠑⠃⠒⣷⣁⡔⠁⠀⣼⢁⠀⡌⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠀⢸⡄⢘⡦⠊⠀⠀⠀⠀⠀⠀⠀⠀⠛⡏⠀⠀⣸⠻⡼⢠⠁⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡏⠀⠀⢈⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣴⢁⠼⠇⢀⡀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠱⠤⢲⠀⠑⣄⣰⠗⠊⠉⠉⠱⡀⠀⠀⠀⢠⠴⠔⢤⣀⠀⠙⢅⠀⠀⣀⠇⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠔⠀⠀⠀⣽⠃⢀⣴⣶⣄⠀⠇⠀⠀⠀⢧⠀⣀⣄⠀⠁⢄⠈⣢⠔⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⠀⠀⠀⣀⡠⠤⠤⣀⡀⠀⠀⠀⣼⠇⠀⡈⣿⣿⣿⡤⠖⠒⠢⢄⣸⣿⣻⣿⢷⠀⠀⢂⠱⡇⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⠀⠀⡠⠖⠉⠀⠀⠀⠀⠀⠉⠓⢄⠀⢿⠀⠀⣿⢿⣿⠏⠀⣤⣤⡀⠀⠙⣿⣿⣿⡿⠀⠀⢸⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⣩⣿⡺⢳⡀⠘⠿⢿⡄⠀⣨⣍⠀⠀⠀⣿⣾⠟⠁⠀⡠⠊⢀⠞⠀⠀⠀⠀⠀⠀⠀⠀",
                "⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠁⠀⣹⠀⠈⢻⣵⣦⣄⠉⠲⣬⣥⡤⠀⠚⠣⠤⠤⢒⣊⣠⠔⢛⠖⠀⠄⡀⠀⠀⠀⠀⠀",
                "⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠇⠀⢀⣼⡿⠈⠈⠉⠛⠛⠛⠛⠛⠒⠒⠛⠛⠛⠻⡿⠄⠈⠢⠑⢄⠀⠀⠀⠀⠀⠀",
                "⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠊⠀⠀⢸⡟⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡟⢄⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀",
                " ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡿⢷⠀⠣⡀⠀⠀⠀⠀⠀⠀⠀⠀",
                "⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠀⡸⠗⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠞⠁⠸⡆⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀",
                "⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠒⢤⣇⠀⠀⠳⣔⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⣿⠀⠀⠛⢄⠀⠀⠀⠀⠀⠀",
                "⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⡠⠃⢸⡆⠀⠀⠈⠷⣦⠀⠀⣀⠰⠟⣡⡤⣤⣄⡀⢠⣇⠀⠀⠀⠀⢻⠑⠠⡀⠀⠀",
                "⠀⠙⣧⠀⠀⠀⠀⠀⠀⡮⠟⢽⢛⠁⢱⠃⣠⡞⣿⣄⣴⠋⠉⢻⡷⢴⠃⠀⢸⠁⠀⠀⠀⠙⢶⡉⠙⠲⣄⠀⠀⢃⠀⠈⢣⠀",
                "⠀⠀⠀⠢⣀⠀⠀⠀⠀⠀⠺⡭⠏⠠⣾⣴⣿⣷⣿⠋⠋⠀⠀⣻⡇⢸⠀⠀⠘⣧⠀⠀⠀⢰⡈⣷⠀⠀⠈⢿⣄⢸⠀⠀⢸⡇",
                "⠀⠀⠀⠀⠈⠳⢀⡀⠀⠀⠬⢧⡦⠀⢳⣾⢯⣽⣿⠀⠀⠀⣰⡟⠀⣿⠀⠀⠀⠸⣧⠀⠀⠈⠓⠛⠀⠀⠀⠰⣿⠏⠀⠀⣾⠇",
                "⠀⠀⠀⠀⠀⢀⣀⣀⣉⣩⣷⣿⣷⣦⣼⣿⡟⢉⡇⠀⠀⢰⡟⠁⢀⡏⠀⠀⠀⢠⣿⣧⡀⠀⠀⠀⠀⠀⣀⣼⣧⣤⡶⠾⠇⠀",
                "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠓⠿⠦⠶⠿⠷⠾⠿⠿⠶⠶⠶⠿⠿⠿⠷⠶⠶⠿⠟⠛⠉⠉⠉⠉⠀⠀⠀ ",
            ],
        )
        return color(panda, 250, 128, 114)


class amazing(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def resise(self, x: int, y: int):
        self.pos = (x, y)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                " _______        ___ ___                          ___             ",
                "|   _   |______|   Y   .---.-.-----.-----.______|   .-----.-----.",
                "|.  1   |______|.      |  _  |-- __|  -__|______|.  |     |  _  |",
                "|.  _   |      |. \_/  |___._|_____|_____|      |.  |__|__|___  |",
                "|:  |   |      |:  |   |                        |:  |     |_____|",
                "|::.|:. |      |::.|:. |                        |::.|            ",
                "`--- ---'      `--- ---'                        `---'            ",
            ],
        )
