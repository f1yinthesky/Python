from typing import List

def splitInHalfImpl(input_list: List[int], current_index: int, sum_so_far: int, half_sum: int) -> int:

    if current_index == len(input_list):
        current_diff = abs(sum(input_list) / 2 - sum_so_far)
        answer_diff = abs(sum(input_list) / 2 - half_sum)
        if current_diff < answer_diff:
            half_sum = sum_so_far
        return half_sum

    sum_so_far_with_add = sum_so_far +input_list[current_index]
    half_sum = splitInHalfImpl(input_list, current_index + 1, sum_so_far_with_add, half_sum)
    half_sum = splitInHalfImpl(input_list, current_index + 1, sum_so_far, half_sum)
    return half_sum

def splitInHalf(input_list: List[int]) -> int:
    half_sum = sum(input_list)
    half_sum = splitInHalfImpl(input_list, 0, 0, half_sum)
    return half_sum


input_list = [1, 2, 3, 10]
print(splitInHalf(input_list))