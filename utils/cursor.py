import os


def cursor(pos: tuple, text: str) -> str:
    return f"\033[{pos[0]};{pos[1]}H{text}"


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
