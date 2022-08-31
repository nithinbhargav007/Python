##Hangman guess the word game
import pyfiglet
import random
result = pyfiglet.figlet_format("Hangman")
print(result)
word=""
list_of_words = ["elephant", "book", "course", "barbeque", "titanium", "cindrella" , "house", "barber" , "dinosuar", "pineapple"]
word = random.choice(list_of_words)
lives=7
count=0

def message(input):
    if input==1:
        print("+++---+++---+++")
        print("              |")
        print("              |")
        print("              |")
        print("              |")
        print("              |")
        print("              |")
        print("              |")
        print("+++---+++---+++")
    elif input==2:
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("              |")
        print("              |")
        print("              |")
        print("              |")
        print("+++---+++---+++")
    elif input==3:
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("     /        |")
        print("              |")
        print("              |")
        print("              |")
        print("+++---+++---+++") 
    elif input==4:
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("     / \      |")
        print("              |")
        print("              |")
        print("              |")
        print("+++---+++---+++")
    elif input==5:
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("     / \      |")
        print("      |       |")
        print("              |")
        print("              |")
        print("+++---+++---+++")
    elif input==6:
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("     / \      |")
        print("      |       |")
        print("     /        |")
        print("              |")
        print("+++---+++---+++")
    elif input==7:
        print("#######   GAME OVER  , HE IS DEAD  ##########")
        print("+++---+++---+++")
        print("      |       |")
        print("      |       |")
        print("      O       |")
        print("     / \      |")
        print("      |       |")
        print("     / \       |")
        print("              |")
        print("+++---+++---+++")

def display_blank(input):
    for i in range(0,len(word)):
        if(word[i]==input and word[i]=="_"):
             word1 = list(word)
             word1[i] = input
             word = ''.join(word1)
             count = count+1
             message(count)
        else:
             word1 = list(word)
             word1[i] = "_"
             word = ''.join(word1)

    
        

input_letter = input("Guess a Letter : ")
display_blank(input_letter)


