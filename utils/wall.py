from abc import ABC, abstractmethod
from .cursor import cursor_more_line


class Wall(ABC):
    def __init__(self, pos: tuple):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    @abstractmethod
    def wall(self) -> str:
        pass


class S(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀█",
                "█    █",
                "█    █",
            ],
        )


class N(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    █",
                "█    █",
                "█▄▄▄▄█",
            ],
        )


class W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "     █",
                "▄▄▄▄▄█",
            ],
        )


class E(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█     ",
                "█▄▄▄▄▄",
            ],
        )


class N_W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    █",
                "     █",
                "▄▄▄▄▄█",
            ],
        )


class E_W(Wall):
    def __init__(self, pos: tuple):
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
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀█",
                "     █",
                "▄    █",
            ],
        )


class S_E(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█▀▀▀▀▀",
                "█     ",
                "█    ▄",
            ],
        )


class S_N(Wall):
    def __init__(self, pos: tuple):
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
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    ▀",
                "█     ",
                "█▄▄▄▄▄",
            ],
        )


class N_E_W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    ▀",
                "      ",
                "▄▄▄▄▄▄",
            ],
        )


class N_S_E(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "█    ▀",
                "█     ",
                "█    ▄",
            ],
        )


class N_S_W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    █",
                "     █",
                "▄    █",
            ],
        )


class S_E_W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀▀▀▀▀▀",
                "      ",
                "▄    ▄",
            ],
        )


class N_S_E_W(Wall):
    def __init__(self, pos: tuple):
        super().__init__(pos)

    def wall(self) -> str:
        return cursor_more_line(
            self.pos,
            [
                "▀    ▀",
                "      ",
                "▄    ▄",
            ],
        )


class Nothing(Wall):
    def __init__(self, pos: tuple):
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


# ██ ▄▄ ▀▀
