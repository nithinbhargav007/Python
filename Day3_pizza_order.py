print("Welcome to automatic Pizza delivery")
size = str(input("Which size of pizza are you looking for? S, M , or L?"))
pni = str(input("do you want to add pepperoni to the Pizza? Y or N? "))
cheese = str(input("Do you want to add extra cheese to the pizza? Y or N?"))
cost = 0 
if(size == "L"):
    cost = 25
elif(size=="M"):
    cost=20
else:
    cost=15

if(pni=='Y' and (size=='L' or size=='M')):
    cost=cost+3
else:
    cost=cost+2

if(cheese=='Y'):
    cost=cost+1

print(f"Your final bill is {cost}$")
