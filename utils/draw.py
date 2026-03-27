from typing import TYPE_CHECKING
from utils import color

if TYPE_CHECKING:
    from parthing import BaseConfig


def info(config: "BaseConfig") -> None:
    print(
        f"""
         CONFIG
      WIDTH = {color(config.Width,150,100,200)}
     HEIGHT = {color(config.Height,140,110,190)}
      ENTRY = x : {color(config.Entry[0],130,120,180)} y : {color(config.Entry[1],130,120,180)}
       EXIT = x : {color(config.Exit[0],120,130,170)} y : {color(config.Exit[1],120,130,170)}
OUTPUT_FILE = {color(config.Output_file,110,140,160)}
    PERFECT = {color(config.Perfect,100,150,150)}

"""
    )
