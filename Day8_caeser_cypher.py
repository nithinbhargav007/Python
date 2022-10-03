alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
input_option = input ( "What do you want to do ?  1. encode    2. decode \n")
input_string = input ("Enter the string : \n")
shift_number = int(input("Enter the shift number : "))


def encode(entered_string, number):
    string2 = []
    for i in range(0,len(entered_string)):
        for j in range(0,len(alphabets)):
            if(entered_string[i]==alphabets[j]):
                string2.append(alphabets[(j+number)%len(alphabets)]) 
                listToStr = ''.join([str(elem) for elem in string2])
    print(listToStr)

def decode(entered_string, number):
    string2 = []
    for i in range(0,len(entered_string)):
        for j in range(0,len(alphabets)):
            if(entered_string[i]==alphabets[j]):
                string2.append(alphabets[(j-number)%len(alphabets)]) 
                listToStr = ''.join([str(elem) for elem in string2])
    print(listToStr)

if(input_option == 'encode'):
    print(f"encode called with shift value {shift_number}")
    encode(input_string, shift_number)
elif(input_option == 'decode'):
    print(f"decode called with shift value {shift_number}")
    decode(input_string, shift_number)
    