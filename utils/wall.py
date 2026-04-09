from abc import ABC, abstractmethod
from .cursor import cursor_more_line


class Wall(ABC):
    def __init__(self, pos: tuple):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def resise(self, x: int, y: int):
        self.pos = (x, y)

    @abstractmethod
    def wall(self) -> str:
        pass


class donjon:
    def enter_or_exit(self) -> str:
        return cursor_more_line(
            (self.x + 1, self.y + 2),
            ["██"],
        )


class S(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀█",
                "█    █",
                "█    █",
            ],
        )


class N(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    █",
                "█    █",
                "█▄▄▄▄█",
            ],
        )


class W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "     █",
                "▄▄▄▄▄█",
            ],
        )


class E(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█     ",
                "█▄▄▄▄▄",
            ],
        )


class N_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    █",
                "     █",
                "▄▄▄▄▄█",
            ],
        )


class E_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "      ",
                "▄▄▄▄▄▄",
            ],
        )


class S_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "     █",
                "▄    █",
            ],
        )


class E_S(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█     ",
                "█    ▄",
            ],
        )


class N_S(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    █",
                "█    █",
                "█    █",
            ],
        )


class N_E(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    ▀",
                "█     ",
                "█▄▄▄▄▄",
            ],
        )


class N_E_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    ▀",
                "      ",
                "▄▄▄▄▄▄",
            ],
        )


class N_E_S(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    ▀",
                "█     ",
                "█    ▄",
            ],
        )


class N_S_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    █",
                "     █",
                "▄    █",
            ],
        )


class E_S_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "      ",
                "▄    ▄",
            ],
        )


class N_E_S_W(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    ▀",
                "      ",
                "▄    ▄",
            ],
        )


class Nothing(Wall, donjon):
    def __init__(self, pos: tuple):
        super().__init__(pos)
        self.entre = False
        self.exit = False

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "██████",
                "██████",
                "██████",
            ],
        )


# ██ ▄▄ ▀▀
