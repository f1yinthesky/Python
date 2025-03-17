""""
Given n = 3, assume that player 1 is "X" and player 2 is "O" in the board.

TicTacToe toe = new TicTacToe(3);

toe.move(0, 0, 1); -> Returns 0 (no one wins)
|X| | |
| | | |    // Player 1 makes a move at (0, 0).
| | | |

toe.move(0, 2, 2); -> Returns 0 (no one wins)
|X| |O|
| | | |    // Player 2 makes a move at (0, 2).
| | | |

toe.move(2, 2, 1); -> Returns 0 (no one wins)
|X| |O|
| | | |    // Player 1 makes a move at (2, 2).
| | |X|

toe.move(1, 1, 2); -> Returns 0 (no one wins)
|X| |O|
| |O| |    // Player 2 makes a move at (1, 1).
| | |X|

toe.move(2, 0, 1); -> Returns 0 (no one wins)
|X| |O|
| |O| |    // Player 1 makes a move at (2, 0).
|X| |X|

toe.move(1, 0, 2); -> Returns 0 (no one wins)
|X| |O|
|O|O| |    // Player 2 makes a move at (1, 0).
|X| |X|

toe.move(2, 1, 1); -> Returns 1 (player 1 wins)
|X| |O|
|O|O| |    // Player 1 makes a move at (2, 1).
|X|X|X|"
"""
from enum import IntEnum
from typing import List

class SpaceStatus(IntEnum):
    UnOccupied = 0
    PlayerOne = 1
    PlayerTwo = 2
    CanNotWin = 3

class TicTacToe:
    board_size: int
    board: List[List[SpaceStatus]]
    win_rows: List[SpaceStatus]
    win_cols: List[SpaceStatus]
    # with size 2
    win_diags: List[SpaceStatus]
    possible_wins: int

    def __init__(self, n:int):
        self.board_size = n
        self.board = [[SpaceStatus.UnOccupied for _ in range(n)] for _ in range(n)]
        self.win_rows = [SpaceStatus.UnOccupied for _ in range(n)]
        self.win_cols = [SpaceStatus.UnOccupied for _ in range(n)]
        self.win_diags = [SpaceStatus.UnOccupied, SpaceStatus.UnOccupied]
        self.possible_wins = 2 * n + 2

    def move(self, row, col, player) -> int:
        current_player = SpaceStatus.PlayerOne if player == 1 else SpaceStatus.PlayerTwo
        other_player = SpaceStatus.PlayerTwo if player == 1 else SpaceStatus.PlayerOne
        assert self.board[row][col] == SpaceStatus.UnOccupied
        self.board[row][col] = current_player
        toe.printBoard()
        if self.possible_wins == 0:
            return 0
        
        # win row
        if self.win_rows[row] == other_player:
            self.win_rows[row] = SpaceStatus.CanNotWin
            self.possible_wins -= 1
        if self.win_rows[row] == SpaceStatus.UnOccupied:
            self.win_rows[row] = current_player
        if self.possible_wins == 0:
            return 0
        if self.win_rows[row] == current_player and all([self.board[row][col_] == current_player for col_ in range(self.board_size)]):
            return int(current_player)
             
        # win col
        if self.win_cols[col] == other_player:
            self.win_cols[col] = SpaceStatus.CanNotWin
            self.possible_wins -= 1
        if self.win_cols[col] == SpaceStatus.UnOccupied:
            self.win_cols[col] = current_player
        if self.possible_wins == 0:
            return 0
        if self.win_cols[col] == current_player and all([self.board[row_][col] == current_player for row_ in range(self.board_size)]):
            return int(current_player)
        
        # win diags
        if row == col:
            if self.win_diags[0] == other_player:
                self.win_diags[0] = SpaceStatus.CanNotWin
                self.possible_wins -= 1
            if self.win_diags[0] == SpaceStatus.UnOccupied:
                self.win_diags[0] = current_player
            if self.possible_wins == 0:
                return 0
            if self.win_diags[0] == current_player and all([self.board[row_][row_] == current_player for row_ in range(self.board_size)]):
                return int(current_player)
        if row + col == self.board_size - 1:
            if self.win_diags[1] == other_player:
                self.win_diags[1] = SpaceStatus.CanNotWin
                self.possible_wins -= 1
            if self.win_diags[1] == SpaceStatus.UnOccupied:
                self.win_diags[1] = current_player
            if self.possible_wins == 0:
                return 0
            if self.win_diags[1] == current_player and all([self.board[row_][self.board_size - 1 - row_] == current_player for row_ in range(self.board_size)]):
                return int(current_player)
        return 0

    def printBoard(self) -> None:
        for row in self.board:
            print(" | ".join([str(int(ele)) for ele in row]))
        print()

toe = TicTacToe(3)

assert toe.move(0, 0, 1) == 0
assert toe.move(0, 2, 2) == 0
assert toe.move(2, 2, 1) == 0
assert toe.move(1, 1, 2) == 0
assert toe.move(2, 0, 1) == 0
assert toe.move(1, 0, 2) == 0
assert toe.move(2, 1, 1) == 1