from typing import List, Optional

def findFirstMismatchPos(previous_stack, current_stack) -> Optional[int]:
    first_mismatch_pos = None
    for i in range(max(len(previous_stack), len(current_stack))):
        if i > len(previous_stack) - 1 or i > len(current_stack) - 1:
            first_mismatch_pos = i
            break
        if previous_stack[i] != current_stack[i]:
            first_mismatch_pos = i
            break
    return first_mismatch_pos

def processLog(log_list: List[str]) -> str:
    log_list.sort()
    call_str = ""
    previous_call_stack = []
    for log in log_list:
        items = log.split(" ")
        call_stack = items[1:]
        first_mismatch_pos = findFirstMismatchPos(previous_call_stack, call_stack)
        if first_mismatch_pos is None:
            continue
        if first_mismatch_pos <= len(previous_call_stack) - 1:
            call_str += " " + " ".join([f"e{fun}" for fun in previous_call_stack[len(previous_call_stack) - 1:first_mismatch_pos - 1:-1]])
        if first_mismatch_pos <= len(call_stack) - 1:
            call_str += " " + " ".join([f"s{fun}" for fun in call_stack[first_mismatch_pos:]])
        previous_call_stack = call_stack
        
    return call_str

def main() -> None:
    input = ["1 A B C", "2 A B D E", "3 A B D E F", "4 A B D", "4.5 A B D", "5 A A A", "6 A B D E"]
    print(processLog(input))


if __name__ == '__main__':
    main()