import random
import time

def do_calculation(left: int, operator: str, right: int, result: int) -> bool:
    print(f"{left}{operator}{right}=")
    answer = int(input())

    if answer == result:
        print ("Correct!\n")
        return True
    else:
        print (f"Wrong!!!!!!!!!!!!!!!!!! The correct answer is {result}.\n")
        return False

def do_one_calculation()->bool:
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)

    add_left=random.randint(1,200)
    add_right = random.randint(1,200)
    add_result = add_left + add_right

    mul_left=random.randint(2,10)
    mul_right = random.randint(1,100)
    mul_result = mul_left * mul_right

    if operator == '+':
        return do_calculation(add_left,'+',add_right, add_result)
    elif operator == '-':
        return do_calculation(add_result,'-',add_left, add_right)
    elif operator == '*':
        return do_calculation(mul_left,'*',mul_right, mul_result)
    else:
        return do_calculation(mul_result,'/',mul_left, mul_right)

print ("We are going to test your basic math skills.")
num_of_questions = int(input("How many questions would you like to answer?\n"))
num_of_correct = 0
num_of_wrong = 0
start_time = time.time()
for i in range(num_of_questions):
    print (f"Question {i+1}:")
    if do_one_calculation():
        num_of_correct = num_of_correct + 1
    else:
        num_of_wrong = num_of_wrong + 1

end_time = time.time()
total_time = end_time - start_time
print (f"Test is over and you have done {num_of_questions} questions in {int(total_time * 100) / 100} seconds.")
print (f"Number of correct answers: {num_of_correct}")
print (f"Number of wrong answers: {num_of_wrong}")
print (f"Percentage of correct answers: {num_of_correct/num_of_questions*100}%")