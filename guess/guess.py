import random

name = input("Hello! What is your name?\n")
print(f"Well, {name}, I'm thinking of a number between 1 and 20.")

target_number = random.randint(1, 20)
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
            print(f"Good job,{name}! You guessed my number in {count} guess!")
        else:    
            print(f"Good job,{name}! You guessed my number in {count} guesses!")
        break

if number != target_number:
    print(f"Nope. The number I was thinking of was {target_number}")
