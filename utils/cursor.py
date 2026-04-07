import os
import curses
import sys
import tty
import termios


def cursor(pos: tuple, text: str) -> str:
    return f"\033[{pos[0]};{pos[1]}H{text}"


def cursor_hide():
    print("\33[?251", end="")


def cursor_shaw():
    print("\33[?25h", end="")


def move_cursor_to_bottom():
    rows = os.get_terminal_size().lines
    print(f"\033[{rows};0H", end="")


def cursor_more_line(pos: tuple, lines: list[str]) -> str:
    result = ""
    for i, line in enumerate(lines):
        result += cursor((pos[0] + i, pos[1]), line)
    return result


def clear() -> None:
    print("\033[2J")
    print("\033[H")


def get_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        # Touches spéciales (flèches etc.) envoient 3 caractères
        if key == "\x1b":
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return key
