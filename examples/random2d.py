import random
from typing import List

def printMatrix(matrix: List[List[int]]) -> None:
    for r in matrix:
        print(", ".join([str(num) for num in r]))
    print("")

def random2d(n: int) -> List[List[int]]:
    result = [[(r+c) % n + 1 for c in range(n)] for r in range(n)]

    #shuffle row
    for current_row in range(n - 1):
        swap_row = random.randint(current_row, n - 1)
        if current_row != swap_row:
            tem = result[current_row]
            result[current_row] = result[swap_row]
            result[swap_row] = tem

    #shuffle col
    for current_col in range(n - 1):
        swap_col = random.randint(current_col, n - 1)
        if current_col != swap_col:
            tem_col_list = [result[r][current_col] for r in range(n)]
            for r in range(n):
                result[r][current_col] = result[r][swap_col]
            for r in range(n):
                result[r][swap_col] = tem_col_list[r]

    return result

printMatrix(random2d(5))