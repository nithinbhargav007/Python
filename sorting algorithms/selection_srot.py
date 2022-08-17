def selection_sort(my_list):
    min_value=my_list[0]
    print(f"initial min value is {min_value}")
    for i in range(0,len(my_list)):
        for j in range(1,len(my_list)):
            if(my_list[j]<my_list[i]):
                min_value=my_list[j]
                my_list[i], my_list[j] = my_list[j], my_list[i]
        print(f'min_value found in first iteration is {min_value}')





my_list = [5,8,0,2,1]
selection_sort(my_list)
print(my_list)
