import random
import time
from typing import Optional
from inputimeout import inputimeout, TimeoutOccurred 

def try_get_int_input(timeout: float) -> Optional[int]:
    try:
        return int(inputimeout(timeout=timeout))
    except (ValueError, TimeoutOccurred) as _e:
        return None


def do_calculation(left: int, operator: str, right: int, result: int, timeout) -> bool:
    print(f"{left} {operator} {right} =")
    answer = try_get_int_input(timeout)

    if answer != result:
        print(f"Wrong!!!!!!!!!!!!!!!!!! The correct answer is {result}.\n")
        return False
    else:
        print("Correct!\n")
        return True


def do_one_calculation(timeout: float) -> bool:
    operators = ["+", "-", "*", "/"]
    operator = random.choice(operators)

    add_left = random.randint(1, 200)
    add_right = random.randint(1, 200)
    add_result = add_left + add_right

    mul_left = random.randint(2, 10)
    mul_right = random.randint(1, 100)
    mul_result = mul_left * mul_right

    if operator == "+":
        return do_calculation(add_left, "+", add_right, add_result, timeout)
    elif operator == "-":
        return do_calculation(add_result, "-", add_left, add_right, timeout)
    elif operator == "*":
        return do_calculation(mul_left, "*", mul_right, mul_result, timeout)
    else:
        return do_calculation(mul_result, "/", mul_left, mul_right, timeout)


print("We are going to test your basic math skills.")
num_of_questions = int(input("How many questions would you like to answer?\n"))
timeout = float(input("How many seconds would you like to spend on each question?\n"))
num_of_correct = 0
num_of_wrong = 0
start_time = time.time()
for i in range(num_of_questions):
    time_so_far = int((time.time() - start_time) * 100) /100
    print(f"time {time_so_far}s Question {i+1}:")
    if do_one_calculation(timeout):
        num_of_correct = num_of_correct + 1
    else:
        num_of_wrong = num_of_wrong + 1

end_time = time.time()
total_time = end_time - start_time
print(
    f"Test is over and you have done {num_of_questions} questions in {int(total_time * 100) / 100} seconds."
)
print(f"Number of correct answers: {num_of_correct}")
print(f"Number of wrong answers: {num_of_wrong}")
print(f"Percentage of correct answers: {int(num_of_correct/num_of_questions*100)}%")
