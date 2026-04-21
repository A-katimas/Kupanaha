from .cursor import cursor, get_key


class Player:
    """
    Represents the player in the maze.

    Handles player position, movement based on keyboard input,
    and rendering in the terminal.
    """

    def __init__(self, pos: list[int], sprite: str) -> None:
        """
        Initialize the player.

        Args:
            pos: Initial position as [row, column].
            sprite: Character or string used to represent the player.
        """
        self.pos = pos
        self.sprite = sprite

    def move(self) -> str:
        """
        Update the player position based on keyboard input.

        Controls:
        - 'z': move up
        - 's': move down
        - 'q': move left
        - 'd': move right

        Returns:
            The key pressed by the user.
        """
        get_move = get_key()
        match (get_move):
            case "z":
                self.pos[0] -= 1
            case "s":
                self.pos[0] += 1
            case "q":
                self.pos[1] -= 2
            case "d":
                self.pos[1] += 2
        return get_move

    def print_self(self) -> None:
        """
        Render the player at its current position in the terminal.
        """
        print(cursor((self.pos[0], self.pos[1]), self.sprite))
