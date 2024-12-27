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
    if choice == computer_choice:
        return "It's a tie!"
    elif choice == 1 and computer_choice == 3:
        return "You win!"
    elif choice == 2 and computer_choice == 1:
        return "You win!"
    elif choice == 3 and computer_choice == 2:
        return "You win!"
    else:
        return "You lose!"
    
print(f"You chose {name_map[choice - 1]}, I chose {name_map[computer_choice - 1]}.\n{get_winner(choice, computer_choice)}")