from .cursor import cursor, get_key


class Player:
    def __init__(self, pos: list[int], sprite: str) -> None:
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

    def print_self(self) -> None:
        print(cursor((self.pos[0], self.pos[1]), self.sprite))
