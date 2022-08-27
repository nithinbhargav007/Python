import random
mylist= input("Please enter list of names separated by comma : ")
l = mylist.split(", ")
person = random.randint(0,len(l))
print(person)
print(f"{l[person]} is going to buy the meal today")