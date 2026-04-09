from .cursor import cursor, get_key


class Player:
    def __init__(self, pos: list, sprite: str) -> None:
        self.pos = pos
        self.sprite = sprite

    def move(self) -> str:
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

    def print_self(self):
        print(cursor(tuple(self.pos), self.sprite))
