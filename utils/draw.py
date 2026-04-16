from tracemalloc import start
from typing import TYPE_CHECKING


from .wall import Wall
from .color import color, bg_color
from .cursor import get_key, clear, move_cursor_to_bottom


# from .player import get_key
from .cursor import cursor_more_line, cursor

import os

if TYPE_CHECKING:
    from utils import Player
    from parthing import BaseConfig

maze_save: list[Wall] | None = None


class Presentation:
    def __init__(self, config: "BaseConfig", player: "Player") -> None:
        from maze.maker import Maze, THEMES

        self.themes = THEMES
        self.scren_size = os.get_terminal_size()
        self.config = config
        self.player = player
        self.info_block = InfoBlock(config, (15, 50))
        self.path = []
        self.start_line = 0
        self.start_col = 0
        self.maze = Maze(
            (config.WIDTH, config.HEIGHT),
            config.ENTRY,
            config.EXIT,
            [12, 35],
            config.THEME,
            config.OUTPUT_FILE,
        )
        self.logo = [
            otter((1, 1)),
            amazing((1, 40)),
            red_panda((1, self.scren_size.columns - 45)),
        ]
        self.start()

    def start(self) -> None:

        lines = (self.maze.size[0] * 3) + 10
        columns = (self.maze.size[1] * 8) + 50

        def good_size(line: int, columns: int) -> list[str]:
            if line >= self.scren_size.lines:
                str_line = color(f"{line}", 255, 0, 0)
            else:
                str_line = color(f"{line}", 0, 255, 0)
            if columns >= self.scren_size.columns:
                str_columns = color(f"{columns}", 255, 0, 0)
            else:
                str_columns = color(f"{columns}", 0, 255, 0)
            return [str_line, str_columns]

        print(
            cursor(
                (27, 50),
                "touch any key to see your screen",
            )
        )

        print(
            self.info_block.block(
                self.maze.get_theme_name(), self.config.PERFECT
            )
        )
        have = good_size(lines, columns)
        print(cursor((13, 50), f"you do have {have[0]} : x   {have[1]} : y"))
        for e in self.logo:
            print(e.wall())

        while True:
            key = get_key()
            if key == "\r" and not (
                self.scren_size.lines <= lines
                and self.scren_size.columns <= columns
            ):
                break
            if key == "q":
                raise ValueError("Good Bey")
            if key == "c":
                self.change_theme()
            if key:
                self.scren_size = os.get_terminal_size()
                clear()
                print(cursor((27, 50), "touch any key to see your screen"))
                print(
                    self.info_block.block(
                        self.maze.get_theme_name(), self.config.PERFECT
                    )
                )
                have = good_size(lines, columns)
                print(
                    cursor(
                        (13, 50), f"you do have {have[0]} : x   {have[1]} : y"
                    )
                )
                self.logo[2].pos = ((1), (self.scren_size.columns - 45))

                for e in self.logo:
                    print(e.wall())

    def loop(self) -> None:
        global maze_save
        set_perfect_mode = self.config.PERFECT
        secondbloc = moveblock((30, 1))
        self.info_block.pos = ((14), (1))
        print(
            self.info_block.block(self.maze.get_theme_name(), set_perfect_mode)
        )
        print(secondbloc.block(set_perfect_mode))
        tile_algo = {
            "prims": self.maze.prims,
            "Prims": self.maze.prims,
            "backtrack": self.maze.backtrack,
            "BackTrack": self.maze.backtrack,
        }
        algo = tile_algo.get(self.config.ALGO)
        if algo:
            algo()
        if not self.config.PERFECT:
            self.maze.make_it_false()
        self.maze.draw_in_folders()
        while True:
            key = get_key()
            if key == "q":
                raise ValueError("Good Bey")
            if key == "c":
                self.change_theme()
                tup_theme = self.maze.get_tuple_theme()
                maze_save = None
                draw_a_maze(
                    self.maze.printable_maze, tup_theme[0], tup_theme[1]
                )
            if key == "b":
                self.maze.make_a_maze()
                maze_save = None
                draw_a_maze(
                    self.maze.printable_maze,
                    self.maze.get_tuple_theme()[0],
                    self.maze.get_tuple_theme()[1],
                )
                maze_save = None
                self.maze.backtrack()
                if not set_perfect_mode:
                    self.maze.make_it_false()
                self.maze.draw_in_folders()

            if key == "i":
                self.maze.make_a_maze()
                maze_save = None
                draw_a_maze(
                    self.maze.printable_maze,
                    self.maze.get_tuple_theme()[0],
                    self.maze.get_tuple_theme()[1],
                )
                maze_save = None
                self.maze.prims()
                if not set_perfect_mode:
                    self.maze.make_it_false()
                self.maze.draw_in_folders()

            if key == "p":
                if set_perfect_mode:
                    set_perfect_mode = False
                else:
                    set_perfect_mode = True

            if key == "l":
                from maze.solver import Solver
                from utils.path_display import PathDrawer
                solve = Solver(self.maze.maze, self.config)
                self.path = solve.solve_maze()
                pathdraw = PathDrawer(self.path)
                pathdraw.path_draw(offset_line=25, offset_col=15)


            if key:
                print(
                    self.info_block.block(
                        self.maze.get_theme_name(), set_perfect_mode
                    )
                )
                print(secondbloc.block(set_perfect_mode))
                move_cursor_to_bottom()

    def change_theme(self) -> None:
        flag = False
        for e in self.themes:
            if flag:
                self.maze.change_theme(e)
                return
            if e == self.maze.get_theme_name():
                flag = True
        self.maze.change_theme(list(self.themes.keys())[0])

    def pressentation_enter(self) -> None:
        pass


class InfoBlock:
    WIDTH = 32

    def __init__(self, config: "BaseConfig", pos: tuple[int, int]) -> None:
        self.pos = pos
        self.config = config

    def block(self, theme: str, perfect: bool) -> str:
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
        screen = f"x : {size.lines}, y : {size.columns}"

        lines = [
            border_top,
            line("         CONFIG"),
            line(f"      WIDTH = {color(c.WIDTH, 150, 100, 200)}"),
            line(f"     HEIGHT = {color(c.HEIGHT, 140, 110, 190)}"),
            line(
                f"      ENTRY = x : {color(c.ENTRY[0], 130, 120, 180)}"
                + f" y : {color(c.ENTRY[1], 130, 120, 180)}",
            ),
            line(
                f"       EXIT = x : {color(c.EXIT[0],  120, 130, 170)}"
                + f" y : {color(c.EXIT[1],  120, 130, 170)}",
            ),
            line(f"OUTPUT_FILE = {color(c.OUTPUT_FILE, 110, 140, 160)}"),
            line(f"    PERFECT = {color(perfect, 100, 150, 150)}"),
            line(f"screen size = {color(screen, 90, 160, 140)}"),
            line(f"       Seed = {color(c.SEED, 80, 170, 130)}"),
            line(f"      Theme = {color(theme, 70, 180, 120)}"),
            line(f" Algorithme = {color(c.ALGO, 80, 170, 140)}"),
            border_bottom,
        ]

        return cursor_more_line(self.pos, lines)


class moveblock:
    WIDTH = 32

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos

    def block(self, perfectmod: bool) -> str:
        w = self.WIDTH

        border_top = "█" + "▀" * w + "█"
        border_bottom = "█" + "▄" * w + "█"
        if perfectmod:
            perfectmod = False
        else:
            perfectmod = True

        # ██ ▄▄ ▀▀
        def line(content: str) -> str:
            import re

            clean = re.sub(r"\x1b\[[0-9;]*m", "", content)
            padding = w - len(clean) - 2
            return "█ " + content + " " * padding + " █"

        lines = [
            border_top,
            line(f"           {color("change", 50, 200, 250)}"),
            line("━" * 30),
            line(f"      -press '{color("q", 50, 200, 100)}' to quit "),
            line("        " + "─" * 15),
            line(f"  -press '{color("c", 50, 200, 100)}' to change theme"),
            line("        " + "─" * 15),
            line(f"   -press '{color("p", 50, 200, 100)}' to change the "),
            line(f"     perfect mode on {color(perfectmod, 90, 160, 150)}"),
            line("        " + "─" * 15),
            line(f"    -press '{color("i", 50, 200, 100)}' to generate"),
            line(f"         a {color("BackTrac", 100, 150, 160)}"),
            line("        " + "─" * 15),
            line(f"    -press '{color("b", 50, 200, 100)}' to generate "),
            line(f"          a {color("Prims", 110, 140, 170)}"),
            line("        " + "─" * 15),
            line(f" -press '{color("l", 50, 200, 100)}' to see the solver "),
            border_bottom,
        ]

        return cursor_more_line(self.pos, lines)


def draw_a_maze(
    maze: list[Wall],
    backcolor: tuple[int, int, int],
    wallcolor: tuple[int, int, int],
) -> None:
    global maze_save
    r = 0
    g = 1
    b = 2

    for i in range(len(maze)):
        if maze_save is None or maze[i] is not maze_save[i]:
            print(
                bg_color(
                    color(
                        maze[i].wall(),
                        backcolor[r],
                        backcolor[g],
                        backcolor[b],
                    ),
                    wallcolor[r],
                    wallcolor[g],
                    wallcolor[b],
                ),
                end="",
            )
            if maze[i].exit is True:
                print(color(maze[i].enter_or_exit(), 50, 200, 50))
            if maze[i].entre is True:
                print(color(maze[i].enter_or_exit(), 200, 100, 50))

    maze_save = list(maze)


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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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


def logo_amazing() -> list[str]:
    return [
        " _______        ___ ___                          ___             ",
        "|       |______|   Y   .---.-.-----.-----.______|   .-----.-----.",
        "|.  Ω   |______|.      |  _  |-- __|  -__|______|.  |     |  _  |",
        "|.  _   |      |. \\_/  |___._|_____|_____|      |.  |__|__|___  |",
        "|:  |   |      |:  |   |                        |:  |     |_____|",
        "|::.|:. |      |::.|:. |                        |::.|            ",
        "`--- ---'      `--- ---'                        `---'            ",
    ]


class amazing(Wall):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__(pos)

    def resise(self, x: int, y: int) -> None:
        self.pos = (x, y)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            logo_amazing(),
        )


