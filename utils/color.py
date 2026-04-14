def color(text: str | int | None, r: int, g: int, b: int) -> str:
    if isinstance(text, str):
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
    return f"\033[38;2;{r};{g};{b}m{str(text)}\033[0m"


def bg_color(text: str | int, r: int, g: int, b: int) -> str:

    if isinstance(text, str):
        return f"\033[48;2;{r};{g};{b}m{str(text)}\033[0m"
    return f"\033[48;2;{r};{g};{b}m{text}\033[0m"
