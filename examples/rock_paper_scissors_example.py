import random

name_map = ["rock", "paper", "scissors"]

choice = int(input(
    """We are going to play rock, paper, scissors.
    Enter your choice:
    1: rock
    2: paper
    3: scissors\n""")
)

computer_choice = random.randint(1, 3)

def get_winner(choice, computer_choice):
    diff = (choice + 3 - computer_choice) % 3
    if diff == 0:
        return "It's a tie!"
    elif diff == 1:
        return "You win!"
    else:
        return "You lose!"
    
print(f"You chose {name_map[choice - 1]}, I chose {name_map[computer_choice - 1]}.\n{get_winner(choice, computer_choice)}")