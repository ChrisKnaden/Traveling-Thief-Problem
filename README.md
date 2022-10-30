# Traveling-Thief-Problem
This problem is about a thief who steals goods from different nodes. He has a maximum weight he can carry, and he must collect the items as quickly
as possible to avoid being caught by the police. The items have different values and weights. The thief has an interest in collecting only the items with the best value/weight ratio in order to make the biggest profit.
To solve this problem, you need to pay attention to the maximum capacity, the value/weight ratio and the shortest way to collect the items.

## Logic of the program
The [Path_Finder.py](Traveling_Thief_Problem/Path_Finder.py) is the main program that calls other methods from different classes.
Before you start the program, you must enter the desired start and end nodes and a text file. The text file is like a map
of places where you can steal goods, and also contains how much weight the thief can carry. The structure of the text file can be seen below. 

After that the text file is loaded by using the class from [Read_File.py](Traveling_Thief_Problem/Read_File.py). 
Based on this data, a list of nodes to visit named ***bb_list*** is created using the class from [Branch_Bound.py](Traveling_Thief_Problem/Branch_Bound.py).

Then, the Path_Finder creates the route for the thief. To do this, it uses the previously specified starting node as the first reference point to get to the next node.
It calculates the distance to each node from the ***bb_list*** using the class of [Dijkstra.py](Traveling_Thief_Problem/Dijkstra.py). 
It then chooses the shortest distance to the next node, changes the current position to the next node, excludes it from the ***bb_list***, and starts searching again for the next node.
This loop ends when every node from the ***bb_list*** has been visited and the final node is reached. The program ends with the output of the solution.

## Example of a textfile
```
#META
name = Problem 0
k = 10 (maximum weight the thief can carry)
N = 7 (total amount of nodes)
#NODES (structure: (coordinates of Node) | (weight, value) | [list of nodes he can go next to])
1   (5,13)  (1,3)  [3] 
2   (15,5)  (2,1)  
3   (8,11)  (2,4)  [1,4,5,6]
4   (11,3)  (3,3)  [1]
5    (3,7)  (2,2)  	
6   (20,6)  (1,1)  [2,3,7]
7   (15,8)  (3,4)  [1,2,4]
#EOF
```

## Example of a solution
Using 6 as the starting node, 7 as the ending node and the text file rtp_0_7.txt from above:


```
Total weight:     10
Total value:      15
Nodes to collect: [1, 3, 4, 6, 7]
nodeList:         [6, 2, 4, 1, 3, 6, 7]
pathLengthList:   [5.099, 4.472, 11.662, 3.606, 13.0, 5.385]
Total distance:   43.224
```
