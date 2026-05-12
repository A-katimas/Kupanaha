from typing import TYPE_CHECKING, Callable, Generator, Any
from types import GeneratorType
import re
import random
from .wall import Wall
from .color import color, bg_color
from .cursor import get_key, clear, move_cursor_to_bottom
from .cursor import cursor_more_line, cursor

import os

if TYPE_CHECKING:
    from utils import Player
    from parthing import BaseConfig

maze_save: list[Wall] | None = None


class Presentation:
    """
    Main controller for rendering and interacting with the maze in the
    terminal.

    Handles:
    - Maze generation and drawing
    - User input (keyboard controls)
    - Theme switching
    - Display of UI blocks (info, controls, logos)
    """

    def __init__(self, config: "BaseConfig", player: "Player") -> None:
        """
        Initialize the presentation system.

        Args:
            config: Configuration object for the maze.
            player: Player instance used for positioning and display.
        """
        from maze.maker import Maze, THEMES

        self.generator: Generator[None, None, None] | None = None
        self.solve: str | None = None
        self.themes = THEMES
        self.scren_size = os.get_terminal_size()
        self.config = config
        self.player = player
        self.info_block = InfoBlock(config, (15, 50))
        self.secondbloc = moveblock((30, 1))
        self.path: Any = []
        self.start_line: int = 0
        self.start_col: int = 0
        self.maze = Maze(
            (config.WIDTH, config.HEIGHT),
            config.ENTRY,
            config.EXIT,
            [12, 35],
            config.THEME,
            config.OUTPUT_FILE,
        )
        self.set_perfect_mode = self.config.PERFECT
        self.logo = [
            otter((1, 1)),
            amazing((1, 40)),
            red_panda((1, self.scren_size.columns - 45)),
        ]
        self.print_modifier: list[Callable[..., str]] = []
        self.itsfalse: bool
        self.start()

    def start(self) -> None:
        """
        Display the initial screen and validate terminal size.

        Waits for user interaction before continuing.
        Allows theme switching and dynamically refreshes the display.
        """

        lines = (self.maze.size[0] * 3) + 10
        columns = (self.maze.size[1] * 8) + 50

        def good_size(line: int, columns: int) -> list[str]:
            """
            Check if the terminal size is sufficient.

            Returns colored values depending on whether the size fits.
            """
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
                (30, 50),
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
            while not (key := get_key()):
                pass
            if key == "\r" and not (
                self.scren_size.lines <= lines
                and self.scren_size.columns <= columns
            ):
                break

            self.key_handler(key, False, [False])
            if not key == "":
                self.scren_size = os.get_terminal_size()
                clear()
                print(cursor((27, 50), "touch any key to see your screen"))
                print(
                    self.info_block.block(
                        self.maze.get_theme_name(), self.set_perfect_mode
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
                print(
                    cursor(
                        (30, 50),
                        "touch any key to see your screen",
                    )
                )

    def loop(self) -> None:
        """
        Main interaction loop.

        Handles:
        - Maze generation (different algorithms)
        - Theme switching
        - Perfect mode toggling
        - Maze solving visualization
        - Redrawing UI elements
        """
        from maze.solver import Solver

        self.info_block.pos = ((14), (1))
        self.startloop()
        path_draw = [False]
        while True:
            key = get_key()
            self.key_handler(key, True, path_draw)
            if key:
                print(
                    self.info_block.block(
                        self.maze.get_theme_name(), self.set_perfect_mode
                    )
                )
                print(self.secondbloc.block(self.set_perfect_mode))
            if maze_save is None:
                draw_a_maze(
                    self,
                    self.maze.printable_maze,
                    self.maze.get_tuple_theme()[0],
                    self.maze.get_tuple_theme()[1],
                    self.path,
                    self.print_modifier,
                    path_draw[0],
                )
            new_maze: bool = False
            try:
                if self.generator is not None:
                    new_maze = True
                    next(self.generator)
                    draw_a_maze(
                        self,
                        self.maze.printable_maze,
                        self.maze.get_tuple_theme()[0],
                        self.maze.get_tuple_theme()[1],
                        self.path,
                        self.print_modifier,
                        False,
                    )
            except StopIteration:
                if (
                    not self.set_perfect_mode
                    and isinstance(self.generator, GeneratorType)
                    and self.generator.gi_code
                    is not self.maze.make_it_false.__code__
                ):
                    self.generator = self.maze.make_it_false()
                else:
                    self.generator = None
                draw_a_maze(
                    self,
                    self.maze.printable_maze,
                    self.maze.get_tuple_theme()[0],
                    self.maze.get_tuple_theme()[1],
                    self.path,
                    self.print_modifier,
                    path_draw[0],
                )
                self.maze.draw_in_folders()
                if new_maze:
                    solve = Solver(self.maze.maze, self.config)
                    self.solve, self.path = solve.solve_maze()
                    with open(f"{self.config.OUTPUT_FILE}", "a+") as output:
                        print("".join(self.solve), file=output)

    def startloop(self) -> None:
        """
        Initialize the main rendering loop and start the selected
        maze generation algorithm.

        This method:
        - Displays the information and control panels
        - Selects the maze generation algorithm from the configuration
        - Creates the corresponding generator used during rendering

        Supported algorithms:
        - ``prims`` / ``Prims``
        - ``backtrack`` / ``BackTrack``

        The selected algorithm is stored as a generator in
        ``self.generator`` and executed progressively in the main loop.
        """
        print(
            self.info_block.block(
                self.maze.get_theme_name(), self.set_perfect_mode
            )
        )
        print(self.secondbloc.block(self.set_perfect_mode))
        tile_algo = {
            "prims": self.maze.prims,
            "Prims": self.maze.prims,
            "backtrack": self.maze.backtrack,
            "BackTrack": self.maze.backtrack,
        }
        algo = tile_algo.get(self.config.ALGO)
        if algo:
            self.generator = algo()

    def key_handler(
        self, key: str, onloop: bool, path_draw: list[bool]
    ) -> None:
        """
        Handle keyboard inputs and trigger the associated maze actions.

        This method processes user key presses to control the application
        behavior, including:
        - quitting the program
        - changing the maze theme
        - generating mazes with different algorithms
        - toggling perfect mode
        - enabling/disabling visual effects
        - showing or hiding the solver path

        Raises:
            ValueError:
                Raised when the user presses ``q`` to quit the program.
        """
        global maze_save

        if key == "q":
            raise ValueError("Good Bey")

        if key == "c" and onloop:
            self.change_theme()
            maze_save = None
            draw_a_maze(
                self,
                self.maze.printable_maze,
                self.maze.get_tuple_theme()[0],
                self.maze.get_tuple_theme()[1],
                self.path,
                self.print_modifier,
                path_draw[0],
            )

        if key == "b" and onloop:
            self.solve = None
            self.path = []
            self.maze.make_a_maze()
            self.generator = self.maze.backtrack()

        elif key == "i" and onloop:
            self.solve = None
            self.path = []
            self.maze.make_a_maze()
            self.generator = self.maze.backtrack()
            self.generator = self.maze.prims()

        elif key == "p":
            if self.set_perfect_mode:
                self.set_perfect_mode = False
            else:
                self.set_perfect_mode = True

        elif key == "h" and onloop:
            if hack in self.print_modifier:
                self.print_modifier.remove(hack)
            else:
                self.print_modifier.append(hack)
            maze_save = None

        elif key == "r" and onloop:
            if inverse in self.print_modifier:
                self.print_modifier.remove(inverse)
            else:
                self.print_modifier.append(inverse)
            maze_save = None

        elif key == "o" and onloop:
            if otter_maker in self.print_modifier:
                self.print_modifier.remove(otter_maker)
            else:
                self.print_modifier.append(otter_maker)
            maze_save = None

        elif key == "l" and onloop:
            if not path_draw[0]:
                path_draw[0] = True
                maze_save = None
            else:
                path_draw[0] = False
                maze_save = None

    def change_theme(self) -> None:
        """
        Cycle through available themes and apply the next one.
        """
        flag = False
        for e in self.themes:
            if flag:
                self.maze.change_theme(e)
                return
            if e == self.maze.get_theme_name():
                flag = True
        self.maze.change_theme(list(self.themes.keys())[0])


def inverse(wall: str) -> str:
    table: dict[int, str | int | None] = {
        ord(" "): "█",
        ord("█"): " ",
        ord("▄"): "▀",
        ord("▀"): "▄",
    }
    return wall.translate(str.maketrans(table))


def hack(wall: str) -> str:
    return re.sub(
        r"[█▄▀]",
        lambda a: chr(random.randrange(32, 127)),
        wall,
    )


def otter_maker(wall: str) -> str:
    return wall.replace("██", "🦦")


class InfoBlock:
    """
    Display block showing configuration and runtime information.
    """

    WIDTH = 32

    def __init__(self, config: "BaseConfig", pos: tuple[int, int]) -> None:
        """
        Initialize the info block.

        Args:
            config: Configuration object.
            pos: Cursor position where the block should be rendered.
        """
        self.pos = pos
        self.config = config

    def block(self, theme: str, perfect: bool) -> str:
        """
        Build the formatted information block.

        Args:
            theme: Current theme name.
            perfect: Whether perfect maze mode is enabled.

        Returns:
            A formatted string ready to be printed.
        """
        size = os.get_terminal_size()
        w = self.WIDTH

        border_top = "█" + "▀" * w + "█"
        border_bottom = "█" + "▄" * w + "█"

        def line(content: str) -> str:
            """
            Format a single line with padding, ignoring ANSI codes length.
            """
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
    """
    Display block showing available controls and actions.

    This block presents keyboard shortcuts to interact with the maze,
    such as quitting, changing theme, toggling modes, and generating mazes.
    """

    WIDTH = 32

    def __init__(self, pos: tuple[int, int]) -> None:
        """
        Initialize the control block.

        Args:
            pos: Cursor position where the block should be rendered.
        """
        self.pos = pos

    def block(self, perfectmod: bool) -> str:
        """
        Build the formatted control/help block.

        Args:
            perfectmod: Current state of the perfect mode.

        Returns:
            A formatted string ready to be printed.
        """
        w = self.WIDTH

        border_top = "█" + "▀" * w + "█"
        border_bottom = "█" + "▄" * w + "█"
        if perfectmod:
            perfectmod = False
        else:
            perfectmod = True

        def line(content: str) -> str:
            """
            Format a single line with padding, ignoring ANSI escape sequences.
            """
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
            line(f"    -press '{color("b", 50, 200, 100)}' to generate"),
            line(f"         a {color("BackTrac", 100, 150, 160)}"),
            line("        " + "─" * 15),
            line(f"    -press '{color("i", 50, 200, 100)}' to generate "),
            line(f"          a {color("Prims", 110, 140, 170)}"),
            line("        " + "─" * 15),
            line(f" -press '{color("l", 50, 200, 100)}' to see the solver "),
            border_bottom,
        ]

        return cursor_more_line(self.pos, lines)


def draw_a_maze(
    press: Any,
    maze: list[Wall],
    backcolor: tuple[int, int, int],
    wallcolor: tuple[int, int, int],
    path_pos: list[Any] = [],
    effect: list[Callable[..., str]] | None = None,
    show_solve: bool = False,
) -> None:
    """
    Renders the maze in the terminal and optionally displays the solution path.

    Only redraws cells that have changed since the last frame, which improves
    performance and reduces flickering. If show_solve is True, overlays an
    emoji along the solution path, chosen based on the current maze theme.

    Args:
        press (Any): The main application object, used to retrieve the
                     current maze theme name.
        maze (list[Wall]): List of Wall objects representing the current
                           state of the maze.
        backcolor (tuple[int, int, int]): RGB color used for the background
                                          of each cell.
        wallcolor (tuple[int, int, int]): RGB color used for the walls
                                          of each cell.
        path_pos (list): List of (x, y) coordinate tuples representing
                         the solution path. Defaults to an empty list.
        effect (list[Callable] | None): Optional list of functions applied
                                        to each wall string before rendering.
                                        Defaults to None.
        show_solve (bool): If True, draws the solution path using a
                           theme-specific emoji. Defaults to False.

    Returns:
        None
    """
    global maze_save
    r = 0
    g = 1
    b = 2
    changed_list = (
        [
            cell
            for cell, old in zip(maze, maze_save)
            if cell.__class__ != old.__class__
        ]
        if maze_save is not None
        else maze
    )

    for changed in changed_list:
        wall = changed.wall()
        for func in effect or []:
            wall = func(wall)
        print(
            bg_color(
                color(
                    wall,
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
        if changed.exit is True:
            print(
                bg_color(
                    changed.enter_or_exit(),
                    wallcolor[r],
                    wallcolor[g],
                    wallcolor[b],
                )
            )
        if changed.entre is True:
            print(
                bg_color(
                    changed.enter_or_exit(),
                    wallcolor[r],
                    wallcolor[g],
                    wallcolor[b],
                )
            )
    if show_solve:
        emoji = {
            "white": "❄️",
            "pink": "🌸",
            "blue": "🐟",
            "green": "🌿",
            "red": "🔥",
            "yellow": "🍌",
            "purple": "🍇",
            "orange": "🍊",
            "cyan": "💎",
            "dark": "🖤",
            "cyberpunk": "🎮",
            "forest": "🌲",
            "ocean": "🏝️",
            "lava": "🌋",
            "gold": "🪙",
            "ice": "🍦",
            "midnight": "🌕",
            "sakura": "🗡️",
            "matrix": "01",
            "sunset": "☀️",
            "neon": "🦋",
            "blood": "🩸",
            "toxic": "💀",
            "sand": "⌛",
            "ash": "♥️",
            "copper": "🥉",
            "arctic": "🌬️",
            "volcano": "🌋",
            "jade": "🐉",
            "rose": "🌹",
            "steel": "⚙️",
            "void": "🎃",
            "ghost": "👻",
            "rust": "🌶️",
            "teal": "🦆",
            "lavender": "🪻",
            "toxic_green": "☘️",
            "deep_sea": "🔮",
            "inferno": "🌪️",
            "snow": "❄︎",
            "poison": "☣️",
            "aurora": "🌅",
            "crimson": "🚓",
        }

        them = press.maze.get_theme_name()

        i = 1
        for pos_x, pos_y in path_pos[0:-1]:
            new_x = (pos_x + path_pos[i][0]) / 2
            new_y = (pos_y + path_pos[i][1]) / 2
            if not (pos_x == 0 and pos_y == 0):
                print(
                    bg_color(
                        color(
                            cursor(
                                (12 + (pos_y * 3) + 1, 35 + (pos_x * 6) + 2),
                                emoji[them],
                            ),
                            backcolor[r],
                            backcolor[g],
                            backcolor[b],
                        ),
                        wallcolor[r],
                        wallcolor[g],
                        wallcolor[b],
                    )
                )

            print(
                bg_color(
                    color(
                        cursor(
                            (12 + int(new_y * 3) + 1, 35 + int(new_x * 6) + 2),
                            emoji[them],
                        ),
                        backcolor[r],
                        backcolor[g],
                        backcolor[b],
                    ),
                    wallcolor[r],
                    wallcolor[g],
                    wallcolor[b],
                )
            )

            if new_x == pos_x:
                print(
                    bg_color(
                        color(
                            cursor(
                                (
                                    12 + int(new_y * 3) + 2,
                                    35 + int(new_x * 6) + 2,
                                ),
                                emoji[them],
                            ),
                            backcolor[r],
                            backcolor[g],
                            backcolor[b],
                        ),
                        wallcolor[r],
                        wallcolor[g],
                        wallcolor[b],
                    )
                )
            i = i + 1
    move_cursor_to_bottom()
    maze_save = maze
    print(flush=True, end="")


class otter(Wall):
    """
    Decorative ASCII art element representing an otter.
    """

    def __init__(self, pos: tuple[int, int]):
        """
        Initialize the otter at a given position.

        Args:
            pos: Cursor position for rendering.
        """
        super().__init__(pos)

    def wall(self) -> str:
        """
        Return the ASCII art of the otter positioned in the terminal.

        Returns:
            A formatted string ready to be printed.
        """
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
    """
    Decorative ASCII art element representing a red panda.
    """

    def __init__(self, pos: tuple[int, int]):
        """
        Initialize the red panda at a given position.

        Args:
            pos: Cursor position for rendering.
        """
        super().__init__(pos)

    def wall(self) -> str:
        """
        Return the ASCII art of the red panda with applied color.

        Returns:
            A formatted string ready to be printed.
        """
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
    """
    Return the ASCII art lines for the 'Amazing' logo.

    Returns:
        A list of strings representing the logo.
    """
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
    """
    Decorative ASCII art element displaying the 'Amazing' logo.
    """

    def __init__(self, pos: tuple[int, int]) -> None:
        """
        Initialize the logo at a given position.

        Args:
            pos: Cursor position for rendering.
        """
        super().__init__(pos)

    def resise(self, x: int, y: int) -> None:
        """
        Update the position of the logo.

        Args:
            x: New row position.
            y: New column position.
        """
        self.pos = (x, y)

    def wall(self) -> str:
        """
        Return the ASCII logo positioned in the terminal.

        Returns:
            A formatted string ready to be printed.
        """
        return cursor_more_line(self.pos, logo_amazing())
