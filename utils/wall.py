from abc import ABC, abstractmethod
from .cursor import cursor_more_line


class Wall(ABC):
    """
    Abstract base class representing a maze tile or visual element.

    Each subclass defines its own ASCII representation via the `wall` method.
    """

    def __init__(self, pos: tuple[int, int]) -> None:
        """
        Initialize a wall element.

        Args:
            pos: Position (row, column) in the terminal.
        """
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.entre = False
        self.exit = False
        self.logowall = False

    def resise(self, x: int, y: int) -> None:
        """
        Update the position of the wall.

        Args:
            x: New row position.
            y: New column position.
        """
        self.pos = (x, y)

    @abstractmethod
    def wall(self) -> str:
        """
        Return the ASCII representation of the wall.

        Must be implemented by subclasses.

        Returns:
            A formatted string ready to be printed.
        """
        pass

    def enter_or_exit(self) -> str:
        """
        Render a marker for entry or exit points.

        Returns:
            A formatted string representing the entry/exit marker.
        """
        return cursor_more_line(
            (self.x + 1, self.y + 2),
            ["🦦"],
        )


class S(Wall):
    """Wall with a southern opening."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "██▀▀██",
                "█    █",
                "█    █",
            ],
        )


class path(Wall):
    """Wall with a southern opening."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "      ",
                "  ██  ",
                "      ",
            ],
        )


# ◢◣◤◥


class N(Wall):
    """Wall with a northern opening."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    █",
                "█    █",
                "██▄▄██",
            ],
        )


class W(Wall):
    """Wall with a western opening."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀██",
                "     █",
                "▄▄▄▄██",
            ],
        )


class E(Wall):
    """Wall with an eastern opening."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "██▀▀▀▀",
                "█     ",
                "██▄▄▄▄",
            ],
        )


class N_W(Wall):
    """Wall with north and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "     █",
                "     █",
                "▄▄▄▄██",
            ],
        )


class E_W(Wall):
    """Wall with east and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "      ",
                "▄▄▄▄▄▄",
            ],
        )


class S_W(Wall):
    """Wall with south and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀██",
                "     █",
                "     █",
            ],
        )


class E_S(Wall):
    """Wall with east and south openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "██▀▀▀▀",
                "█     ",
                "█     ",
            ],
        )


class N_S(Wall):
    """Wall with north and south openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    █",
                "█    █",
                "█    █",
            ],
        )


class N_E(Wall):
    """Wall with north and east openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█     ",
                "█     ",
                "██▄▄▄▄",
            ],
        )


class N_E_W(Wall):
    """Wall with north, east, and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "      ",
                "      ",
                "▄▄▄▄▄▄",
            ],
        )


class N_E_S(Wall):
    """Wall with north, east, and south openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█     ",
                "█     ",
                "█     ",
            ],
        )


class N_S_W(Wall):
    """Wall with north, south, and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "     █",
                "     █",
                "     █",
            ],
        )


class E_S_W(Wall):
    """Wall with east, south, and west openings."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "      ",
                "      ",
            ],
        )


class N_E_S_W(Wall):
    """Wall with all four directions open (empty passage)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "      ",
                "      ",
                "      ",
            ],
        )


# ▄▀


class Nothing(Wall):
    """
    Fully filled tile (no passage), typically used as a solid block.
    """

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "██████",
                "██████",
                "██████",
            ],
        )


class petit_logo42(Wall):
    """
    Small decorative '42' logo element.
    """

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "╻ ╻┏━┓",
                "┗━┫┏━┛",
                "  ╹┗━╸",
            ],
        )


class gros_logo42_0(Wall):
    """Large '42' logo segment (part 0)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀█",
                "█ ██ █",
                "█ ██ █",
            ],
        )


class gros_logo42_1(Wall):
    """Large '42' logo segment (part 1)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█ ██ █",
                "█ ██ █",
                "█ ██ █",
            ],
        )


class gros_logo42_2(Wall):
    """Large '42' logo segment (part 2)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█ ██ ▀",
                "█ ████",
                "█▄▄▄▄▄",
            ],
        )


class gros_logo42_3(Wall):
    """Large '42' logo segment (part 3)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "██████",
                "▄▄▄▄▄▄",
            ],
        )


class gros_logo42_4(Wall):
    """Large '42' logo segment (part 4)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "████ █",
                "▄ ██ █",
            ],
        )


class gros_logo42_5(Wall):
    """Large '42' logo segment (part 5)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█ ██ █",
                "█ ██ █",
                "█ ██ █",
            ],
        )


class gros_logo42_6(Wall):
    """Large '42' logo segment (part 6)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█ ██ █",
                "█ ██ █",
                "█▄▄▄▄█",
            ],
        )


class gros_logo42_7(Wall):
    """Large '42' logo segment (part 7)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█ ████",
                "█▄▄▄▄▄",
            ],
        )


class gros_logo42_8(Wall):
    """Large '42' logo segment (part 8)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀ ██ █",
                "████ █",
                "▄▄▄▄▄█",
            ],
        )


class gros_logo42_9(Wall):
    """Large '42' logo segment (part 9)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█ ████",
                "█ ██ ▄",
            ],
        )


class gros_logo42_10(Wall):
    """Large '42' logo segment (part 10)."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "████ █",
                "▄▄▄▄▄█",
            ],
        )
