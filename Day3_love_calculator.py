name1=str(input("Please enter the first Name : "))
name2= str(input("Please enter the second Name : "))
str1 = "true"
str2= "love"
count1 =0
count2= 0

for i in range(0,len(name1)):
    for j in range(0,len(str1)):
        if(name1[i]==str1[j]):
            count1=count1+1

for i in range(0,len(name2)):
    for j in range(0,len(str1)):
        if(name2[i]==str1[j]):
            count1=count1+1

for i in range(0,len(name1)):
    for j in range(0,len(str2)):
        if(name1[i]==str2[j]):
            count2=count2+1

for i in range(0,len(name2)):
    for j in range(0,len(str2)):
        if(name2[i]==str2[j]):
            count2=count2+1

print(f"overall score is {count1}{count2}%")