from calendar import week


age = int(input("What is your Age?\n"))
days_left = (90-age)*365
months_left = (90-age)*12
weeks_left = (90-age)*52

print(f"You have {days_left} days,{weeks_left} weeks, and {months_left} months left ")