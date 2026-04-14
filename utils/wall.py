from abc import ABC, abstractmethod
from .cursor import cursor_more_line


class Wall(ABC):
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.entre = False
        self.exit = False
        self.logowall = False

    def resise(self, x: int, y: int) -> None:
        self.pos = (x, y)

    @abstractmethod
    def wall(self) -> str:
        pass

    def enter_or_exit(self) -> str:
        return cursor_more_line(
            (self.x + 1, self.y + 2),
            ["██"],
        )


class S(Wall):
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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


class E_S(Wall):
    def __init__(self, pos: tuple[int, int]):
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


class N_S(Wall):
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
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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


class N_E_S(Wall):
    def __init__(self, pos: tuple[int, int]):
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
    def __init__(self, pos: tuple[int, int]):
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


class E_S_W(Wall):
    def __init__(self, pos: tuple[int, int]):
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


class N_E_S_W(Wall):
    def __init__(self, pos: tuple[int, int]):
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


# ██ ▄▄ ▀▀


# ┏━┓┗┛┣┫┃
