from typing import TYPE_CHECKING
from utils.wall import *
from utils import color
from .cursor import cursor

if TYPE_CHECKING:
    from parthing import BaseConfig


def info(config: "BaseConfig", pos: tuple) -> None:
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
            ],
        )
    )


def a_maze(maze: list[Wall]):
     for i in maze:
        print(i.wall(), end="")
