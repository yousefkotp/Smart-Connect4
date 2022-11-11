import math

import numpy as np

# 1: max, 0 min


class Board:
    def __init__(self):
        self.state = 1 << 63
        self.maxDepth = 1
        self.mapStates = {}
        self.bestMove = {}

    def getDepth(self):
        return self.maxDepth

    def setDepth(self, depth):
        self.maxDepth = depth


BOARD = Board()

"""
1- Good heuristic function aka make the function a linear weighted sum of the features
2- Transpositional Table
3- Save moves for early game -> first 6 turns
4- use multi-processing if we can
5- Enhance the exploring order by exploring best moves first aka moves which places new item near to existing one
"""


def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def getLastLocationMask(state, col):
    return ((7 << (60 - (9 * col))) & state) >> (60 - (9 * col))


def decimalToBinary2(n):
    return "{0:b}".format(int(n))


# Check if the state makes the board full
def isGameOver(state):
    k = 60
    for j in range(0, 7):
        maxLocation = (((7 << k) & state) >> k)
        if maxLocation != 7:
            return False
        k -= 9
    return True


def convertToTwoDimensions(state):
    twoDimensionalArray = np.full((6, 7), -1, np.int8)

    k = 60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        lastLocation = getLastLocationMask(state, j) - 1
        k -= 9
        for row in range(0, lastLocation):
            currentBit = ((1 << (startingBits[j] - row)) & state) >> (startingBits[j] - row)
            twoDimensionalArray[row][j] = currentBit
    return twoDimensionalArray


def convertToNumber(twoDimensionalState):
    n = 1 << 63
    k = 60
    startingBits = [59, 50, 41, 32, 23, 14, 5]
    for j in range(0, 7):
        flag = False
        for i in range(0, 6):
            if twoDimensionalState[i][j] == 1:
                n = set_bit(n, startingBits[j] - i)
            elif twoDimensionalState[i][j] == -1:
                n = (((i + 1) << k) | n)
                flag = True
                break
        if not flag:
            n = ((7 << k) | n)
        k -= 9
    return n


#
# print(sys.getsizeof(convertToTwoDimensions(10378549747953762464)))


# 3  points for 4 -sure point
# 2  points for 3 -candidate point
# 1  point  for 2 -candidate point
# -4 points for 4 -sure opponent point
# -3 points for 3 -candidate opponent point
# -2 points for 2 -candidate opponent point


# the value is




def check_neigbours(x, y, value, array):
    if value==1:
        other_player=0
    else:
        other_player=1
    cost = 0
    map = {}
    map[value] = 1
    map[-1] = 0
    map[other_player]=-50
    if x <= 2:
        temp = 0
        for i in range(0, 4):
            temp += map[array[x + i][y]]
        if temp > 1:
            if (value == 1):
                print(str(temp) + " first cond")
            else:
                print("-" + str(temp) + " first cond")
            cost += temp
        if temp == -47:
            cost-=1
            print(" -1 y pasha")

    if y <= 3:
        temp = 0
        for i in range(0, 4):
            if array[x][y + i] not in map:
                temp += -50
            else:
                temp += map[array[x][y + i]]
        if temp > 1:
            if (value == 1):
                print(str(temp) + " second cond")
            else:
                print("-" + str(temp) + " second cond")
            cost += temp
        if temp == -47:
            cost-=1
            print(" -1 y pasha")

    if x <= 2 and y <= 3:
        temp = 0
        for i in range(0, 4):
            if array[x + i][y + i] not in map:
                temp += -50
            else:
                temp += map[array[x + i][y + i]]
        if temp > 1:
            if (value == 1):
                print(str(temp) + " third cond")
            else:
                print("-" + str(temp) + " third cond")
            cost += temp
        if temp == -47:
            cost-=1
            print(" -1 y pasha")

    if x <= 2 and y >= 3:
        temp = 0
        for i in range(0, 4):
            if array[x + i][y - i] not in map:
                temp += -50
            else:
                temp += map[array[x + i][y - i]]
            print("--"+str(temp)+"---")
        if temp > 1:
            if (value == 1):
                print(str(temp) + " fourth cond")
            else:
                print("-" + str(temp) + " fourth cond")
            cost += temp
        if temp == -47:
            cost-=1
            print(" -2 y pasha")

    if value == 1:
        return cost
    else:
        return -cost


def heuristic(state):
    print("------------------new state ------------------------")
    array = convertToTwoDimensions(state)
    print(array)
    value = 0
    for i in range(0, 6):
        for j in range(0, 7):
            print(str(i) + "-" + str(j))
            if array[i][j] != -1:
                value += check_neigbours(i, j, array[i][j], array)
    print("----------------------------value is : "+str(value))
    return value


# max =1
# min =0
# print(heuristic(int("1011100000100100000101110000100111000010100000011110000010100000", 2)))

def getChildren(player, state):
    list=[33,42,24,51,15,60,6]
    # k = 60
    children = []
    for i in range(0, 7):
        k=list[i]
        temp_state = state
        temp = ((7 << k) & temp_state) >> k
        if player == 1 and temp != 7:
            temp_state = state | (1 << (k - temp))
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            children.append(temp_state)
        elif player == 0 and temp != 7:
            temp_state = clear_bit(temp_state, k - temp)
            temp_state = clear_bit(temp_state, k)
            temp_state = clear_bit(temp_state, k + 1)
            temp_state = clear_bit(temp_state, k + 2)
            temp_state = temp_state | ((temp + 1) << k)
            children.append(temp_state)
        # k -= 9
    return children

def miniMax(maxDepth, depth, isMaxPlayer, state):
    if depth == maxDepth or isGameOver(state):
        return state, heuristic(state)

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
        BOARD.bestMove[state] = maxChild
        return maxChild, maxValue
    else:
        minChild = None
        minValue = math.inf
        for child in children:
            childValue = miniMax(maxDepth, depth + 1, not isMaxPlayer, child)[1]
            if childValue < minValue:
                minValue = childValue
                minChild = child
        return minChild, minValue


def miniMaxAlphaBeta(maxDepth, depth, isMaxPlayer, state, alpha, beta):
    if depth == maxDepth or isGameOver(state):
        return state, heuristic(state)

    children = getChildren(isMaxPlayer, state)
    BOARD.mapStates[state] = children
    if isMaxPlayer:
        maxChild = None
        maxValue = -math.inf

        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, False, child, alpha, beta)[1]
            if childValue > maxValue:
                maxChild = child
                maxValue = childValue
            if maxValue >= beta:
                break
            if maxValue > alpha:
                alpha = maxValue
        BOARD.bestMove[state] = maxChild
        return maxChild, maxValue
    else:
        minChild = None
        minValue = math.inf
        for child in children:
            childValue = miniMaxAlphaBeta(maxDepth, depth + 1, True, child, alpha, beta)[1]
            if childValue < minValue:
                minValue = childValue
                minChild = child
            if minValue <= alpha:
                break
            if minValue < beta:
                beta = minValue
        return minChild, minValue


def nextMove(alphaBetaPruning, state):  # The function returns the next best state in integer form
    # if state in BOARD.bestMove.keys():
    #     return BOARD.bestMove[state]
    if alphaBetaPruning:
        return miniMaxAlphaBeta(BOARD.maxDepth, 0, True, state, -math.inf, math.inf)[0]
    return miniMax(BOARD.maxDepth, 0, True, state)[0]


# temp = np.full((6, 7), -1, np.int8)
# print(temp.itemsize)
# print(temp.size)
# print(sys.getsizeof(temp))


# print(heuristic(12114687404279889984))
# print("\n")
# nextState = nextMove(0,12114687404279889984)
# print(convertToTwoDimensions(nextState))
# print(heuristic(nextState))
# print("\n")
# print(heuristic(12117079941581930560))


# getChildren(1, int("1010100000010100000010100000010100000010100000010100000010100000", 2))
# print((int("1010100000010100000010100000010100000010100000010100000010100000",2)))
# print(bin(1010100000010100000010100000010100000010100000010100000010100000))
# print(intoBinary(int("1010100000010100000010100000010100000010100000010100000010100000",2)))
# DecimalToBinary(int("1010100000010100000010100000010100000010100000010100000010100000",2))
# print(string)


# print(heuristic(int("1011100000100100000101110000100111000010100000011110000010100000", 2)))

# print(heuristic(int("1011100000100100000101110000100111000010100000001000000001000000", 2)))
# print(sys.getsizeof(convertToTwoDimensions(int("1011100000100100000101110000100111000010100000001000000001000000", 2))))
# print(heuristic(int("1010100000010100000010100000010100000010100000010100000010100000",2)))
