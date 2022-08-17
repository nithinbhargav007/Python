#insertion sort
# This sort starts from the beginning and compares 2 elements at a time
# swaps the elements if the criteria is not met


def insertion_sort(my_list):
    for i in range(1,len(my_list)):
        for j in range(i-1,-1,-1):
            if my_list[j+1]<my_list[j]:
                my_list[j+1],my_list[j] = my_list[j],my_list[j+1]
            else:
                break

my_list = [4,3,2,1]
insertion_sort(my_list)
print(my_list)

