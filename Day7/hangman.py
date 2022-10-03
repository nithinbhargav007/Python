import pyfiglet
import random
result = pyfiglet.figlet_format("Hangman")
print(result)
word=""
list_of_words = ["elephant", "book", "course", "barbeque", "titanium", "cindrella" , "house", "barber" , "dinosuar", "pineapple"]
word = random.choice(list_of_words)