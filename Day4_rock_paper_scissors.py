import random
my_choice = int(input("What do you chose?  1 for rock, 2 for paper, 3 for scissors"))
computer_choice= random.randint(1,3)
if(my_choice ==computer_choice):
    print(f"Its a draw. You chose {my_choice} and computer chose {computer_choice}")
elif(my_choice==1 and computer_choice==2):
    print(f"You win.You chose {my_choice} and computer chose {computer_choice} ")
elif(my_choice==1 and computer_choice==3):
    print(f"You win.You chose {my_choice} and computer chose {computer_choice} ")
elif(my_choice==2 and computer_choice==1):
    print(f"You loose.You chose {my_choice} and computer chose {computer_choice} ")
elif(my_choice==2 and computer_choice==3):
    print(f"You loose.You chose {my_choice} and computer chose {computer_choice} ")
elif(my_choice==3 and computer_choice==1):
    print(f"You loose.You chose {my_choice} and computer chose {computer_choice} ")
elif(my_choice==3 and computer_choice==2):
    print(f"You loose.You chose {my_choice} and computer chose {computer_choice} ")