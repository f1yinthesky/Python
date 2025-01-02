import random
print ("We are going to play rock, paper, scissors.")
print ("""Enter your choice:
       1:rock
       2:paper
       3:scissors""")


choice = input()
while choice not in {'1', '2', '3'}:
    print ("Invalid choice. Please try again.")
    choice = input()
choice=int(choice)

AI_choice = random.randint(1,3)

print(f"Your choice is {choice}. My choice is {AI_choice}.")

if choice == 1:
    if AI_choice == 1:
        print ("It's a tie!")
    elif AI_choice == 2:
        print ("You lose!")
    else:
        print ("You win!")

elif choice == 2:
    if AI_choice == 2:
        print ("It's a tie!")
    elif AI_choice == 3:
        print ("You lose!")
    else:
        print ("You win!")


else:
    if AI_choice == 3:
        print ("It's a tie!")
    elif AI_choice == 1:
        print ("You lose!")
    else:
        print ("You win!")