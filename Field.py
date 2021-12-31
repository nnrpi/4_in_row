class Field:

    def __init__(self) -> None:
        self.used = [0 for x in range(7)]
        self.cells = [[2 for i in range(6)] for j in range(7)]

    def _put_chip(self, col: int, player: bool) -> bool:
        if self.used[col] >= 7:
            return False
        self.cells[col][self.used[col]] = player
        self.used[col] += 1
        return True

    def _check_horizontals(self, player: bool) -> bool:
        for row in range(6):
            for col in range(4):
                if self.cells[col][row] == self.cells[col + 1][row] == self.cells[col + 2][row] == self.cells[col + 3][row] == player:
                    return True
        return False

    def _check_verticals(self, player: bool) -> bool:
        for col in range(7):
            for row in range(3):
                if self.cells[col][row] == self.cells[col][row + 1] == self.cells[col][row + 2] == self.cells[col][row + 3] == player:
                    return True
        return False

    def _check_diagonals1(self, player: bool) -> bool:
        for col in range(4):
            for row in range(3):
                if self.cells[col][row] == self.cells[col + 1][row + 1] == self.cells[col + 2][row + 2] == self.cells[col + 3][row + 3] == player:
                    return True
        return False

    def _check_diagonals2(self, player: bool) -> bool:
        for col in range(3, 7):
            for row in range(3):
                if self.cells[col][row] == self.cells[col - 1][row + 1] == self.cells[col - 2][row + 2] == self.cells[col - 3][row + 3] == player:
                    return True
        return False

    def _check_win(self, player: bool) -> bool:
        return self._check_horizontals(player) or self._check_verticals(player) or self._check_diagonals1(player) or self._check_diagonals2(player)

    def __str__(self):
        field_str = ""
        for row in range(5, -1, -1):
            for col in range(7):
                if self.cells[col][row] == 2:
                    field_str += "E"
                elif self.cells[col][row] == 0:
                    field_str += "F"
                else:
                    field_str += "S"
            field_str += "\n"
        return field_str

    def turn(self, col: int, player: bool) -> int:
        if not self._put_chip(col, player):
            return 2
        return self._check_win(player)