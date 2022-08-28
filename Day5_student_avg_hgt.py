student_heights=[180,124,165,173,189,169,146]
total=0
for height in range(0,len(student_heights)):
    total = student_heights[height] + total

avg_height = total/len(student_heights)
print(f"the average student height is {avg_height}")
print(f"the average student height rounded  is {round(avg_height)}")