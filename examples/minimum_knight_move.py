"""
In an infinite  chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].

A knight has 8 possible moves it can make, as illustrated below. Each move is two squares in a cardinal direction, then one square in an orthogonal direction.

Return the minimum number of steps needed to move the knight to the square [x, y].  It is guaranteed the answer exists.
"""

def printBoard(board):
    for row in board:
        print(row)

def minimum_knight_move(x:int, y:int) -> int:
    x = abs(x)
    y = abs(y)

    board = [[3*(row + col) for col in range(max(4, y + 1))] for row in range(max(4,x+1))]
    board[0][0] = 0
    board[0][1] = 3
    board[0][2] = 2
    board[0][3] = 3

    board[1][0] = 3
    board[1][1] = 2
    board[1][2] = 1
    board[1][3] = 2

    board[2][0] = 2
    board[2][1] = 1
    board[2][2] = 4
    board[2][3] = 3

    board[3][0] = 3
    board[3][1] = 2
    board[3][2] = 3
    board[3][3] = 2

    if x <=3 and y <= 3:
        return board[x][y]

    from queue import PriorityQueue
    candidates = PriorityQueue()

    candidates.put((2, (0,2)))
    candidates.put((3, (0,3)))
    candidates.put((1, (1,2)))
    candidates.put((2, (1,3)))
    candidates.put((2, (2,0)))
    candidates.put((1, (2,1)))
    candidates.put((4, (2,2)))
    candidates.put((3, (2,3)))
    candidates.put((3, (3,0)))
    candidates.put((2, (3,1)))
    candidates.put((3, (3,2)))
    candidates.put((2, (3,3)))
    
    visited_nodes = {(0,0),(0,1),(1,0),(1,1)}


    while not candidates.empty():
        (num_jump, pos) = candidates.get()
        (current_x, current_y) = pos
        visited_nodes.add(pos)
        if pos == (x, y):
            return num_jump
        next_nodes = [(current_x + 1, current_y + 2),
                      (current_x - 1, current_y + 2),
                      (current_x + 2, current_y + 1),
                      (current_x - 2, current_y + 1),
                      (current_x + 2, current_y - 1),
                      (current_x - 2, current_y - 1),
                      (current_x + 1, current_y - 2),
                      (current_x - 1, current_y - 2)]
        next_nodes = [pos for pos in next_nodes if 0 <= pos[0] and pos[0] <= x and 0 <= pos[1] and pos[1] <= y and pos not in visited_nodes]
        for next_node in next_nodes:
            if next_node == (x, y):
                return num_jump + 1
            candidates.put((num_jump + 1, next_node))

    return 0

assert minimum_knight_move(0, 0) == 0
assert minimum_knight_move(1, 0) == 3
assert minimum_knight_move(0, -1) == 3
assert minimum_knight_move(1, 2) == 1
assert minimum_knight_move(-1, -1) == 2
assert minimum_knight_move(3, -3) == 2
assert minimum_knight_move(-4, 4) == 4
assert minimum_knight_move(5, -5) == 4
assert minimum_knight_move(-2, -5) == 3
assert minimum_knight_move(6, -5) == 5