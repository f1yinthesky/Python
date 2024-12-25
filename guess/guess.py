import random

name = input("Hello! What is your name?\n")
min_num = 6
max_num = 150
print(f"Well, {name}, I'm thinking of a number between {min_num} and {max_num}.")
target_number = random.randint(min_num, max_num)
max_count = 8
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
