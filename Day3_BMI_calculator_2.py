height = float(input("Enter your height in metre : "))
weight = float(input("Enter your weight in Kg : "))
BMI = weight/height**2
print(f"You BMIis {BMI}")
if(BMI<18.5):
    print("You are underweight")
elif(BMI > 18.5 and BMI<25):
    print("Congrats, you have a normal weight")
elif(BMI>25 and BMI<30):
    print("You are overweight")
elif(BMI>30 and BMI<35):
    print("You are obese")
else:
    print("You are clinically obese")