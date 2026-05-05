from parthing import parth
from utils import (
    color,
    clear,
    Presentation,
)
from utils.player import Player
import random
from utils.cursor import move_cursor_to_bottom
import sys


folders_exist = True
try:
    open("config.txt", "r")

except FileNotFoundError as e:
    print(e)
    folders_exist = False


def main() -> None:
    """
    Entry point of the application.

    This function:
    - Validates command-line arguments
    - Loads and parses the configuration file
    - Initializes the random seed
    - Creates the player instance
    - Starts the presentation loop

    If an error occurs during execution, it is displayed at the bottom
    of the terminal.
    """
    if len(sys.argv) < 2:
        print(
            color(
                f"Usage: uv run python3 {sys.argv[0]} (configfolders.txt)"
                + " or make run (configfolders.txt)",
                255,
                200,
                200,
            )
        )
        sys.exit(1)

    config = parth(sys.argv[1])

    if config is not None:
        clear()
        random.seed(config.SEED)

        icones_joueur = {"sakura": "👘", "halloween": "👻", "default": "🦦"}
        mon_sprite = icones_joueur.get(config.THEME, "🦦")

        player = Player([config.ENTRY[0], config.ENTRY[1]], mon_sprite)

        try:
            press = Presentation(config, player)
            press.loop()
        except ValueError as e:
            move_cursor_to_bottom()
            print(e)


if __name__ == "__main__":
    """
    Script execution guard.

    Ensures that the program only runs if the required configuration
    file exists.
    """
    if folders_exist:
        main()
