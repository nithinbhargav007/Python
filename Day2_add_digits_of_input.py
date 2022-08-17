

def find_sum(number):
    total=0
    for i in range (0,len(number)):
        total = total + int(number[i])
    return total

number = str(input("Please enter a number : "))
print("The total sum is"+ str(find_sum(number)))
