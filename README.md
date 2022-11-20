# Connect4
Intelligent Agent to play Connect-4 with a modifiable depth.

## Table of Content
- [connect4](#connect4)
  * [Deployment](#deployment)
  * [State Representation](#state-representation)
  * [MiniMax Algorithm](#minimax-algorithm)
  * [Data Structures Used](#data-structures-used)
  * [Optimizations](#optimizations)
    + [Heuristic Pruning](#heuristic-pruning)
    + [Alpha-Beta Pruning](#alpha-beta-pruning)
      - [Pseudocode](#pseudocode)
    + [Exploring Best Moves First](#exploring-best-moves-first)
  * [Analysis for Runtime](#analysis-for-runtime)
    + [Without Pruning](#without-pruning)
    + [With Pruning](#with-pruning)
  * [MiniMax Tree Visualizer](#minimax-tree-visualizer)
  * [Graphical Interface](#graphical-interface)
    + [Landing Interface](#landing-interface)
    + [Game Interface](#game-interface)
    + [Settings Interface](#settings-interface)
  * [Contributors](#contributors)
## Deployment

- The project was built using [Python 3.9](https://www.python.org/downloads/release/python-390/), make sure you configure your python interpreter correctly
- You should run the "interface.py" python file, you can do that by running the following command inside the project folder
 ```bash
  python interface.py
 ```


## State Representation
- The simplest way to represent the board is using a 2D array. However, using 2D array uses ( $6\times 7\times size of integer$ ). This representation would limits the agent by only reaching short search depth and doesn't enable the agent to go deep in the search tree.
- The board configuration (state) is represented as 64-bit number as each column takes 9 bits and is represented as follows:
    - A 3 bits for each column which points to the last empty location, we can call them last location mask, for example if the three bits is "001" indeicates that the next location is the first row
    - A 6 bits representing each slot inside that column, 0 for the human and 1 for the intelligent agent.
    - The 64th bit indicates whether the state is pruned or not, it is only useful when printing the search tree so we can neglect it in most of our operations (check the [Alpha Beta Pruning](#alpha-beta-pruning) section for a better understanding).
- We can conclude from the previous representation that an empty board will be represented as the bits:
    > 1 001000000 001000000 001000000 001000000 001000000 001000000 001000000
- Those bits are equal to the number "10378549747928563776" in decimal.

- Actions are implemented by incrementing the last location mask of every column and upating the bit corresponding to that slot.


## MiniMax Algorithm

- MiniMax Algorihm Pseudocode:
  ```python
    Function MiniMax(maxDepth, currentDepth, isMaxPlayer, state)
        if currentDepth == maxDepth
            return state,heuristic(state)
        if isGameOver(state)
            return state,getFinalScore(state)
        
        children = getChilder(state)
        if isMaxPlayer // if it is the agent's turn
            Initialize maxChild, maxValue with negative infinity
            for child in children
                childValue = MiniMax(maxDepth,currentDepth+1, not isMaxPlayer, child)[1]
                if childValue > maxValue
                    maxChild = child, maxValue = childValue
            return maxChild, maxValue
        else
            Initialize minChild, minValue with positive infinity
            for child in children
                childValue = MiniMax(maxDepth,currentDepth+1, not isMaxPlayer, child)[1]
                if childValue < minValue
                    minChild = child, minValue = childValue
            return minChild, minValue
  ```
## Data Structures Used
- Hash map to map from states to its children (next states).
- Hash map to map from states to its values.

## Optimizations
- Since that branching factor in connect-4 is 7, and the depth is 42, then the total number of states to search is 7^42 which is nearly equals 3x10^35 state. The agent needs to use some pruning to enhance the runtime and work in real time.

### Heuristic Pruning
- Heuristic pruning is a modified version of minimax algorithm used in games that has high branching factor of states and high depth.
- We simulate the game until certain depth (entered by the user) and then we calculate the heuristic value that estimates the power of current states compared to other states to choose the best choice according to the minimax algorithm
- Certain weighting criteria is developed by us to evaluate the strength of the moves.
- In this Program we offer 2 heuristics:
- The more intuitive and simple one:
   - Positive part
     * 4 consecutive (AI color) gets 4 points
     * 3 candidate consecutive (AI color) gets 3 points
     * 2 candidate consecutive (AI color) gets 2 points
     * stopping opponent from getting a point gets 1 point
   - Negative part
     * 4 consecutive (Human color) gets -4 points
     * 3 candidate consecutive (Human color) gets -3 points
     * 2 candidate consecutive (Human color) gets -2 points
     * stopping AI from getting a point gets -1 point
- The more aware heuristic :
   - Positive part
     * 4 consecutive (AI color) gets 40 points
     * 3 candidate consecutive (AI color) gets 17 points (next move will gaurantee the point)
     * 3 candidate consecutive (AI color) gets 15 points (a colomn is not build yet)
     * 2 candidate consecutive (AI color) gets 4 points (next move will gaurantee the point)
     * 2 candidate consecutive (AI color) gets 2 points (a colomn is not build yet)
     * stopping opponent from getting a point gets 13 point
   - Negative part
     * 4 consecutive (Human color) gets -40 points
     * 3 candidate consecutive (Human color) gets -17 points (next move will gaurantee the point)
     * 3 candidate consecutive (Human color) gets -15 points (a colomn is not build yet)
     * 2 candidate consecutive (Human color) gets -4 points (next move will gaurantee the point)
     * 2 candidate consecutive (Human color) gets -2 points (a colomn is not build yet)
     * stopping AI from getting a point gets -13 point
    
### Alpha-Beta Pruning
- Alpha-Beta pruning is a modified version of the minimax algorithm to optimize it.
- Alpha-Beta can be a real game changer, it cannot eliminate the exponent, but it can cuts it to half.
- Alpha-Beta Pruning can -without checking each node of the game tree- compute the correct minimax decision. This involves two threshold parameter Alpha and beta for future expansion, so it is called alpha-beta pruning.
    * Alpha: The best (highest-value) choice we have found so far at any point along the path of Maximizer. The initial value of alpha is -∞.
    * Beta: The best (lowest-value) choice we have found so far at any point along the path of Minimizer. The initial value of beta is +∞.
- The condition for the pruning is: α>=β 
> Alpha is only updated by Max Player, while Beta is only updated by Min player.
#### Pseudocode

  ```python
    Function MiniMaxAlphaBeta(maxDepth, currentDepth, isMaxPlayer, state, alpha,beta)
        if currentDepth == maxDepth
            return state,heuristic(state)
        if isGameOver(state)
            return state,getFinalScore(state)
        
        children = getChilder(state)
        if isMaxPlayer // if it is the agent's turn
            Initialize maxChild, maxValue with negative infinity
            for child in children
                childValue = MiniMax(maxDepth,currentDepth+1, not isMaxPlayer, child)[1]
                if childValue > maxValue
                    maxChild = child, maxValue = childValue
                if maxValue > alpha:
                    alpha = maxValue
                if alpha >= beta:
                    break
            return maxChild, maxValue
        else
            Initialize minChild, minValue with positive infinity
            for child in children
                childValue = MiniMax(maxDepth,currentDepth+1, not isMaxPlayer, child)[1]
                if childValue < minValue
                    minChild = child, minValue = childValue
                if minValue < beta:
                    beta = minValue
                if beta <= alpha:
                    break
            return minChild, minValue

  ```
### Exploring Best Moves First
- A lot of research regarding the connect-4 game has shown that playing in the middle or near the middle enhances the chances of winning the game, playing in the middle is considered in a lot of time the best choice.
- Exploring a state where we place a piece in the middle firstly has enhanced the alpha-beta pruning quite well especially in early game.

## Analysis for Runtime
- The following anlaysis is done on some random states, so the numbers can varies from one state to another in case of pruning.
- The time is measured in seconds.

### Without Pruning
<table align="center">
  <tr>
    <th>Depth</th>
    <th>States Expanded</th>
    <th>Time Taken</th>

  </tr>
  <tr>
    <td>1</td>
    <td>8</td>
    <td>0.001</td>
  </tr>
  <tr>
    <td>2</td>
    <td>57</td>
    <td>0.007</td>
  </tr>
  <tr>
    <td>3</td>
    <td>400</td>
    <td>0.069</td>
  </tr>
  <tr>
    <td>4</td>
    <td>2775</td>
    <td>0.521</td>
  </tr>
  <tr>
    <td>5</td>
    <td>19608</td>
    <td>3.01</td>
  </tr>
</table>

### With Pruning

<table align="center">
  <tr>
    <th>Depth</th>
    <th>States Expanded</th>
    <th>Time Taken</th>
  </tr>
  <tr>
    <td>1</td>
    <td>8</td>
    <td>0.001</td>
  </tr>
  <tr>
    <td>2</td>
    <td>27</td>
    <td>0.005</td>
  </tr>
  <tr>
    <td>3</td>
    <td>84</td>
    <td>0.013</td>
  </tr>
  <tr>
    <td>4</td>
    <td>235</td>
    <td>0.115</td>
  </tr>
  <tr>
    <td>5</td>
    <td>1111</td>
    <td>0.645</td>
  </tr>
</table>

## MiniMax Tree Visualizer

![me](https://github.com/adhammohamed1/connect4/blob/main/Tree-Visualizer.gif)

## Graphical Interface
### Landing Interface

![image](https://user-images.githubusercontent.com/41492875/202769630-24a76e93-53f6-40d7-9059-975f254698fb.png)

### Game Interface

![image](https://user-images.githubusercontent.com/41492875/202769769-9c29ff52-0e7b-4242-887b-1dd988664c50.png)

### Settings Interface

![settingsss](https://user-images.githubusercontent.com/90573502/202927516-db42e77c-f47a-4af2-bfbb-6cb53a103b47.jpg)

## Contributors

1- [Yousef Kotp](https://github.com/yousefkotp)

2- [Adham Mohammed](https://github.com/adhammohamed1)

3- [Mohammed Farid](https://github.com/MohamedFarid612)
