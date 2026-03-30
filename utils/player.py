from .cursor import cursor


class Player:
    def __init__(self, pos: tuple) -> None:
        self.pos = pos
        pass

    def move(self):
        print(cursor(self.pos, "❤️"))
