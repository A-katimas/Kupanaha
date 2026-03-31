from typing import TYPE_CHECKING
from .wall import *
from .color import color

# from .player import get_key
from .cursor import cursor_more_line

import os

if TYPE_CHECKING:
    from maze.maker import Maze
    from utils import Player
    from parthing import BaseConfig


class Presentation:
    def __init__(self, config: "BaseConfig", mazeing: "Maze", player: "Player"):
        self.config = config
        self.mazeing = mazeing
        self.player = player
        self.info_block = InfoBlock(config, (15, 15))
        self.start()

    def start(self):
        print(self.info_block.wall())

    def loop(self):
        self.info_block.pos=((1),(1))
        print(self.info_block.wall())


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


def info(config: "BaseConfig", pos: tuple):
    size = os.get_terminal_size()
    print(
        cursor_more_line(
            pos,
            [
                "         CONFIG",
                f"      WIDTH = {color(config.Width,150,100,200)}",
                f"     HEIGHT = {color(config.Height,140,110,190)}",
                f"      ENTRY = x : {color(config.Entry[0],130,120,180)} y : {color(config.Entry[1],130,120,180)}",
                f"       EXIT = x : {color(config.Exit[0],120,130,170)} y : {color(config.Exit[1],120,130,170)}",
                f"OUTPUT_FILE = {color(config.Output_file,110,140,160)}",
                f"    PERFECT = {color(config.Perfect,100,150,150)}",
                f"screen size = {color(f"x : {size.lines - 10},y : {size.columns - 10}",90,160,140)} ",
            ],
        )
    )


def a_maze(maze: list[Wall], backcolor: tuple, wallcolor: tuple):
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
