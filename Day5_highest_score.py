

def find_max_score(list):
    max_score=0
    for score in list:
        if(score>max_score):
            max_score=score
    return max_score

print(f"The highest score in the class is : {find_max_score([78,91,82,111,45,67])}")