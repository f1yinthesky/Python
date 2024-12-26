import random
import math

name = input("Hello! What is your name?\n")
min_num = int(input(f"Well, {name}, what is the minimum number you want to guess?\n"))
max_num = int(input(f"Well, {name}, what is the maxium number you want to guess?\n"))
print(f"Well, {name}, I'm thinking of a number between {min_num} and {max_num}.")
target_number = random.randint(min_num, max_num)
max_count = max(1, math.ceil(math.log2(max_num - min_num + 2)))
count = 0
while count < max_count:
    number = int(input("Take a guess.\n"))
    count = count + 1
    print(f"The number of guesses you have made is {count}.")
    if number < target_number:
        print("Your guess is too low.")
    elif number > target_number:
        print("Your guess is too high.")
    else:
        if count == 1:
            print(f"Good job, {name}! You guessed my number in {count} guess!")
        else:    
            print(f"Good job, {name}! You guessed my number in {count} guesses!")
        break
if number != target_number:
    print(f"Nope. The number I was thinking of was {target_number}")
