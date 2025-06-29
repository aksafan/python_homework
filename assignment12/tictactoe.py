class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message


class Board:
    valid_moves = ["upper left", "upper center", "upper right", "middle left", "center", "middle right", "lower left",
                   "lower center", "lower right"]

    def __init__(self):
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.X = "X"
        self.O = "O"
        self.turn = self.X

    def __str__(self):
        result = []
        for x in self.board_array:
            result.append(" | ".join(x))

        return "\n---------\n".join(result)

    def move(self, move_string):
        if move_string not in self.valid_moves:
            raise TictactoeException("That's not a valid move.")

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][column] = self.turn

        self.change_turn()

    def whats_next(self):
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break

        if cat:
            return True, "Cat's Game"

        win = False
        for i in range(3): # check rows
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] and self.board_array[i][1] == self.board_array[i][2]:
                    win = True
                    break
        if not win:
            for i in range(3): # check columns
                if self.board_array[0][i] != " ":
                    if self.board_array[0][i] == self.board_array[1][i] and self.board_array[1][i] == self.board_array[2][i]:
                        win = True
                        break
        if not win:
            if self.board_array[1][1] != " ": # check diagonals
                if self.board_array[0][0] ==  self.board_array[1][1] and self.board_array[2][2] == self.board_array[1][1]:
                    win = True
                if self.board_array[0][2] ==  self.board_array[1][1] and self.board_array[2][0] == self.board_array[1][1]:
                    win = True

        if not win:
            return False, "X's turn" if self.turn == self.X else "O's turn"
        else:
            return True, "X has won" if self.turn == self.O else "O has won"

    def change_turn(self):
        self.turn = self.O if self.turn == self.X else self.X


print("Welcome to the Tictactoe game\n")
board = Board()
print(board)
result, message = False, ""

while not result:
    valid_move = input(f"What is your next move? Valid moves are: {",".join(board.valid_moves)}\n")

    try:
        board.move(valid_move)
    except TictactoeException as e:
        print(e)
        print(board)
        _, message = board.whats_next()
        print(message)

        continue

    result, message = board.whats_next()
    print(board)
    print(message)
