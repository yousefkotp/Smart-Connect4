import math
import interface

# 1: max, 0 min


class Board:
    def __init__(self):
        self.state = 1 << 63
        self.maxDepth = interface.DEPTH
        self.mapStates = {}


BOARD = Board()

"""
1- Good heuristic function aka make the function a linear weighted sum of the features
2- Transpositional Table
3- Save moves for early game -> first 6 turns
4- use multi-processing if we can
5- Enhance the exploring order by exploring best moves first aka moves which places new item near to existing one
"""


def decimalToBinary2(n):
    return "{0:b}".format(int(n))


def convertToTwoDimensions(state):
    twoDimensionalArray = []

    for i in range(0, 6):
        twoDimensionalArray.insert(i, [-1, -1, -1, -1, -1, -1, -1])
    k = 60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        lastLocation = (((7 << k) & state) >> k) - 1
        k -= 9
        for row in range(0, lastLocation):
            currentBit = ((1 << (startingBits[j] - row)) & state) >> (startingBits[j] - row)
            twoDimensionalArray[row][j] = currentBit
    return twoDimensionalArray




def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)

def convertToNumber(twoDimensionalState):
    n = 17309616014371291584 # Equivalent to 111000000 for each column
    k=60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        for i in range(0, 6):
            if twoDimensionalState[i][j] == 1:
                n = set_bit(n, startingBits[j] - i)
            elif twoDimensionalState[i][j]==-1:
                n = (((j+1) << (k)) & n)
        k-=9
    return n

# max =1
# min =0


def getChildren(player, state):
    print(decimalToBinary2(state))
    k = 60
    children = []
    for i in range(0, 7):
        temp_state = state
        temp = ((7 << (k)) & temp_state) >> (k)
        if player == 1 and temp != 7:
            temp_state = state | (1 << (k - temp))
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            print(decimalToBinary2(temp_state))
            children.append(temp_state)
        elif player == 0 and temp != 7:
            temp_state = clear_bit(temp_state, k - temp)
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            children.append(temp_state)
            print(decimalToBinary2(temp_state))
        k -= 9
    return children


def nextMove(alphaBetaPruning, state):  # The function returns the next best state in integer form
    if alphaBetaPruning:
        return miniMaxAlphaBeta(BOARD.maxDepth, 0, 1, state, -math.inf, math.inf)[0]
    return miniMax(BOARD.maxDepth, 0, 1, state)[0]


def miniMax(maxDepth, depth, isMaxPlayer, state):
    if depth == maxDepth or isGameOver(state):
        return (state, getValue(state))

    children = getChildren(isMaxPlayer, state)
    BOARD.mapStates[state] = children
    if isMaxPlayer:
        maxChild = None
        maxValue = -math.inf
        for child in children:
            childValue = miniMax(maxDepth, depth + 1, not isMaxPlayer, child)[1]
            if childValue > maxValue:
                maxChild = child
                maxValue = childValue
        return (maxChild, maxValue)
    else:
        minChild = None
        minValue = math.inf
        for child in children:
            childValue = miniMax(maxDepth, depth + 1, not isMaxPlayer, child)[1]
            if childValue > minValue:
                minValue = childValue
                minChild = child
        return (minChild, minValue)


def miniMaxAlphaBeta(maxDepth, depth, isMaxPlayer, state, alpha, beta):
    if depth == maxDepth or isGameOver(state):
        return (state, getValue(state))

    if isMaxPlayer:
        maxChild = None
        maxValue = -math.inf
        children = getChildren(isMaxPlayer, state)
        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, not isMaxPlayer, child, alpha, beta)[1]
            if childValue > maxValue:
                maxChild = child
                maxValue = childValue
            if maxValue >= beta:
                break
            if maxValue > alpha:
                alpha = maxValue
        return (maxChild, maxValue)
    else:
        minChild = None
        minValue = math.inf
        children = getChildren(isMaxPlayer, state)
        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, not isMaxPlayer, child, alpha, beta)[1]
            if childValue > minValue:
                minValue = childValue
                minChild = child
            if minValue <= alpha:
                break
            if minValue < beta:
                beta = minValue
        return (minChild, minValue)


# Check if the state makes the board full
def isGameOver(state):
    k = 60
    for j in range(0, 7):
        maxLocation = (((7 << k) & state) >> k)
        if maxLocation != 7:
            return False
        k -= 9
    return True


# Fitness/Heuristic Function
def getValue(state):
    return True


getChildren(1, int("1010100000010100000010100000010100000010100000010100000010100000", 2))
# print((int("1010100000010100000010100000010100000010100000010100000010100000",2)))
# print(bin(1010100000010100000010100000010100000010100000010100000010100000))
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
