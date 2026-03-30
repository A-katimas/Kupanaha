def cursor(pos: tuple, text: str) -> str:
    return f"\033[{pos[0]};{pos[1]}H{text}"


def cursor_more_line(pos:tuple ,lines: list[str]) -> str:
    result = ""
    for i, line in enumerate(lines):
        result += cursor((pos[1] + i, pos[0]), line)
    return result


def clear() -> None:
    print("\033[2J")
    print("\033[H")
