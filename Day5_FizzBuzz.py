for i in range(1,101):
    if(i%3 == 0 and i%5!=0):
        print(f"Number is {i} , Fizz")
    elif(i%5==0 and i%3!=0):
        print(f"Number is {i} , Buzz")
    elif(i%3==0 and i%5==0):
        print(f"Number is {i} , FizzBuzz")