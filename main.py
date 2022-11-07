

#1100
#k-1
# print(1<<2&12)
# # 1 010100000 010100000 010100000 010100000 010100000 010100000 010100000 

# x=int('0101000000101000000101000000101000000101000000101000000101000001', 2)
# print(x) 
# print(len('0101000000101000000101000000101000000101000000101000000101000001'))

# #law 3ayez agib el rakam el fl awel 
# # awl makan
# print(1<<63 & x)
# print(1<<(54) & x)
#awl  makan k=63 62 61    (60,59,58,57,56,55)
#tany makan k=54 53 52    (56,56,56,56,56,56)
# tany
# string=""
# def DecimalToBinary(num):
#         global string
#         if num >= 1:
#             DecimalToBinary(num // 2)
#             string+=str( (num % 2) )
        
# def printBinaryVal(num):
#     global string    
#     DecimalToBinary(num)
#     print(string)
#     string=""
#     return

def decimalToBinary2(n):
    return "{0:b}".format(int(n))


def getChildren(next_color,state):
    print(decimalToBinary2(state))
    # printBinaryVal(state)
    k=62
    arr=[]
    for i in range(0,7):
        temp=((7<<(k-2))&state)>>(k-2)
        # print(temp)
        state=state| (1<<(k-temp-2))
        print(decimalToBinary2(state))
        k-=9
    return arr

# print("-----------")
# for i in range(0,9):
#     print(i)

#kosom el byson
getChildren(1,int("1010100000010100000010100000010100000010100000010100000010100000",2))
# print((int("1010100000010100000010100000010100000010100000010100000010100000",2)))
#print(bin(1010100000010100000010100000010100000010100000010100000010100000))
# print(intoBinary(int("1010100000010100000010100000010100000010100000010100000010100000",2)))
# DecimalToBinary(int("1010100000010100000010100000010100000010100000010100000010100000",2))
# print(string)




# ---------------------------------------------------------------------

# def getChildren(next_color,state):
#     global string
#     DecimalToBinary(state)
#     print(string)
#     string=""
#     k=62
#     arr=[]
#     arkam=[]
#     for i in range(0,7):
#         next_zero_binary=""
#         # print(111<<(k-2))
#         # DecimalToBinary(111<<(k-2))
#         # print(string)
#         # string=""
#         temp=((7<<(k-2))&state)>>(k-2)
#         print(temp) 
#         # if(1<<k & state):
#         #      next_zero_binary+="1"
#         # else:
#         #      next_zero_binary+="0"
#         # if(1<<(k-1) & state):
#         #      next_zero_binary+="1"
#         # else:
#         #      next_zero_binary+="0"
#         # if(1<<(k-2) & state):
#         #      next_zero_binary+="1"
#         # else:
#         #      next_zero_binary+="0"      



#         # arr.append(next_zero_binary)
#         # state=state| (1<<(k-int(next_zero_binary,2)-2))
#         state=state| (1<<(k-temp-2))

#         DecimalToBinary(state)
#         print(string)
#         string=""

#         k-=9

#     #     arkam.append(int(next_zero_binary,2))

#     # print(arr)
#     # print(arkam)                

#     return arr
