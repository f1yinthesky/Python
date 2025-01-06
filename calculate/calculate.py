import random

print ("We are going to test your basic math skills.")

operators = ['+']
operator = random.choice(operators)

add_left=random.randint(1,50)
add_right = random.randint(1,50)
add_result = add_left + add_right

print(f"{add_left}+{add_right}=")
answer = int(input())

if answer == add_result:
    print ("Correct!")
else:
    print (f"Wrong! The correct answer is {add_result}.")