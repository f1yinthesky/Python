"""
Input:
board =
[[110,5,112,113,114],[210,211,5,213,214],[310,311,3,313,314],[410,411,412,5,414],[5,1,512,3,3],[610,4,1,613,614],[710,1,2,713,714],[810,1,2,1,1],[1,1,2,2,2],[4,1,4,4,1014]]

Output:
[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[110,0,0,0,114],[210,0,0,0,214],[310,0,0,113,314],[410,0,0,213,414],[610,211,112,313,614],[710,311,412,613,714],[810,411,512,713,1014]]"
"""

from typing import List

def printBoard(board:List[List[int]]) -> None:
    for row in board:
        print("  ".join([f"{num:3n}" for num in row]))

def isRowLine(start_col: int, row:int,  board:List[List[int]]) -> bool:
    if start_col + 2 >= len(board[0]):
        return False
    return abs(board[row][start_col]) == abs(board[row][start_col + 1]) and abs(board[row][start_col]) == abs(board[row][start_col + 2]) and abs(board[row][start_col + 2]) > 0

def isColLine(start_row: int, col:int, board:List[List[int]]) -> bool:
    if start_row + 2 >= len(board):
        return False
    return abs(board[start_row][col]) == abs(board[start_row + 1][col]) and abs(board[start_row][col]) == abs(board[start_row + 2][col]) and abs(board[start_row + 2][col]) > 0

def discoverElimination(board:List[List[int]]) -> bool:
    discovered = False
    for row in range(len(board)):
        for col in range(len(board[0])):
            if isRowLine(col, row, board):
                board[row][col] = -abs(board[row][col])
                board[row][col + 1] = -abs(board[row][col + 1])
                board[row][col + 2] = -abs(board[row][col + 2])
                discovered = True
            if isColLine(row, col, board):
                board[row][col] = -abs(board[row][col])
                board[row + 1][col] = -abs(board[row + 1][col])
                board[row + 2][col] = -abs(board[row + 2][col])
                discovered = True
    return discovered   

def eliminate(board:List[List[int]]) -> None:
    for col in range(len(board[0])):
        new_row = len(board) - 1
        row = len(board) - 1
        while new_row >= 0:
            if row >= 0:
                if board[row][col] > 0:
                    board[new_row][col] = board[row][col]
                    new_row -= 1
                row -= 1
            else:
                board[new_row][col] = 0
                new_row -= 1

def crash(board:List[List[int]]) -> None:
    while True:
        #print("before discover")
        #printBoard(board)
        has_elimination = discoverElimination(board)
        #print("after discover")
        #printBoard(board)
        if not has_elimination:
            break
        eliminate(board)
        #print("after eliminate")
        #printBoard(board)
        #print("")
    return

board = [[110,5,112,113,114],[210,211,5,213,214],[310,311,3,313,314],[410,411,412,5,414],[5,1,512,3,3],[610,4,1,613,614],[710,1,2,713,714],[810,1,2,1,1],[1,1,2,2,2],[4,1,4,4,1014]]
crash(board)
assert board == [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[110,0,0,0,114],[210,0,0,0,214],[310,0,0,113,314],[410,0,0,213,414],[610,211,112,313,614],[710,311,412,613,714],[810,411,512,713,1014]]

board = [[1,2], [1,2], [1,2]]
crash(board)
assert board == [[0,0],[0,0],[0,0]]