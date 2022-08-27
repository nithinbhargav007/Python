row1=["🔷","🔷","🔷"]
row2=["🔷","🔷","🔷"]
row3=["🔷","🔷","🔷"]

mylist=[row1,row2,row3]
print(mylist)
x=input("Where do you want to put the treasure? : ")
row=int(x[1])
col=int(x[0])
mylist[row][col] = "🟡"
print(mylist)