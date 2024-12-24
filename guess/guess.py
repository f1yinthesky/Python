
name = input("Hello! What is your name?\n")
print(f"Well, {name}, I'm thinking of a number between 1 and 20.")

target_number = 8
number = int(input("Take a guess.\n"))
count =1

if number < target_number:
    print("Your guess is too low")
if number > target_number:
    print("Your guess is too high")
if number == target_number:
    print(f"Good job,{name}! You guessed my number in {count} guess!")