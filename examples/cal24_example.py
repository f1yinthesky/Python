def normalized_tuple(input_tuple):
    return tuple(sorted(input_tuple))

def get_next_tuple_candidates(input_tuple):
    candidates = set()
    for i in range(len(input_tuple)):
        for j in range(i+1, len(input_tuple)):
            right, left = input_tuple[i], input_tuple[j]
            left_over = tuple([input_tuple[k] for k in range(len(input_tuple)) if k != i and k != j])
            
            sum = right + left
            candidates.add(normalized_tuple((sum,) + left_over))

            diff_1 = right - left
            candidates.add(normalized_tuple((diff_1,) + left_over))

            diff_2 = left - right
            candidates.add(normalized_tuple((diff_2,) + left_over))

            product = right * left
            candidates.add(normalized_tuple((product,) + left_over))

            if left != 0:
                quotient_1 = right / left
                candidates.add(normalized_tuple((quotient_1,) + left_over))
            if right != 0:
                quotient_2 = left / right
                candidates.add(normalized_tuple((quotient_2,) + left_over))
            
    return candidates        

def print_result(target_tuple, input, parent_dict):
    print("Solution found!")
    solution_path = []
    current = target_tuple
    while current != input:
        solution_path.append(current)
        current = parent_dict[current]
    solution_path.append(input)
    solution_path.reverse()
    solution_string = " --> ".join(str(node) for node in solution_path)
    print(solution_string)

def cal24(input_tuple):
    assert len(input_tuple) > 1
    sorted_input = normalized_tuple(input_tuple)

    target_tuple = (24,)

    candidates_pool = [sorted_input]
    visited = set()
    parent_dict = {}

    while len(candidates_pool) > 0:
        candiate = candidates_pool.pop()
        if candiate in visited:
            continue
        visited.add(candiate)

        if candiate == target_tuple:
            print_result(target_tuple, sorted_input, parent_dict)
            return
        
        if candiate == tuple():
            continue

        next_candidates = get_next_tuple_candidates(candiate)
        for next_candidate in next_candidates:
            if next_candidate not in visited:
                candidates_pool.append(next_candidate)
                parent_dict[next_candidate] = candiate
    print("No solution found!")

while True:
    input_str = input("Please input more than 1 numbers separated by comma: \n")
    input_tuple = tuple(int(x) for x in input_str.split(","))
    cal24(input_tuple)
    if input("Do you want to continue? (Y/N)\n").lower() != "y":
        break