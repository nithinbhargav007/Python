#this program splits the bill across N people considering the top percentage(x%) into account

print("Welcome to the tip calculator. \n");
total_bill = float(input("What was the total bill in rupees? $"))
num_people= int(input("You want to split the bill with how many people?"))
percentage_tip=int(input("What percentage of tip would you like to give? \n 1. 10 \n 2. 20 \n 3. 30 \n"))
each_person = float((total_bill * (1 + percentage_tip/100)) / num_people)
print("Each Person should pay "+ str(each_person)+ " /- Rupees")