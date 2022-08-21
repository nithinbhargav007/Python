year = int(input("Enter the year of interest : "))
print(f"the value of year is {year}")

if(year % 4 == 0):
    if((year%100 != 0) | (year%400==0)):
            print("Its a leap year")
    else:
            print("its not a leap year")
else:
    print("Its not a leap year")