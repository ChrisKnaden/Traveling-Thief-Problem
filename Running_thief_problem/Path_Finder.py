import Read_File
import Branch_Bound
import Dijkstra
import math

'''
Main Class for the Running-Thief-Problem
'''
class Path_Finder(object):
    '''
    Constructor that reads the .txt file and uses the Branch and Bound algorithm to find the optimal Nodes to collect.
    start: Starting Node
    end: Ending Node
    filename: .txt file with information about location of Nodes and weight restriction (k)
    items: List, that contains the (weight, value) of an object, that can be collected
    neighbours: List of neighbours of each Node [neighbour1, neighbour2...]
    coordinates: List, that contains every location (x,y) of each Node, in the same order as in the .txt file
    ratioed_items: List of value/weight ratio of items [(value/weight, weight, value, itemNumber),...]
    max_capacity: The maximum capacity, that the thief can lift, it's "k" of the .txt file
    bb_list: List with locations to collect the optimal amount of goods, 1 to collect, 0 to ignore
    graph: List with distance from one node to each other node
    '''
    def __init__(self, start, end, filename):
        self.start = start
        self.end = end
        rf = Read_File.Read_File(filename)
        self.items, self.neighbours, self.coordinates, self.ratioed_items, self.max_capacity = rf.readInstance()
        bb = Branch_Bound.Branch_Bound(self.items, self.max_capacity, self.ratioed_items)
        self.bb_list = bb.executeBB()
        self.graph = self.convertToGraph()

    '''
    Output the total weight, total value and all locations, that have to be collected.
    totalWeight: The total weight
    totalValue: The total value
    locationsToCollect: List of locations with their Node-Name, which have to be collected
    weight: Weight of the item
    value: Value of the item
    '''
    def outputGeneralData(self):
        totalWeight = totalValue = 0
        locationsToCollect = []
        for i, element in enumerate(self.bb_list):
            if element == 1:
                locationsToCollect.append(i + 1)
                weight, value = self.items[i]
                totalWeight += weight
                totalValue += value

        print("Gesamtgewicht:   ", totalWeight)
        print("Gesamtpreis:     ", totalValue)
        print("Sammelorte:      ", locationsToCollect)
        return

    '''
    Creates a route along the different nodes from the list, that the Branch and Bound has created.
    First, general data collected from the Branch and Bound algorithm is printed.
    Then the nodeList is calculated. After that the nodeList is printed.
    '''
    def createRoute(self):
        self.outputGeneralData()
        nodeList = self.getNodeList
        self.outputSolution(nodeList)
        return

    '''
    Creates the route and returns the nodeList.
    searchElement: Is responsible for the termination of the method. As long the searchElemnt is 1, there is still a "1"
                   left in the bb_list. If there is only a "2" left, searchElement is set to 2.
    nodeList: List of Nodes the thief has to visit in this particular order, starting with the starting node
    compPathList: List to compare the different path length's with each other, just for the decision from one node to
                  the next node
    indexPathList: List with the index of the specific node, correlating to the compPathList
    startIndex: The node from which the Dijkstra algorithm starts searching for the next closest node
    sPath: Shortest Path's
    pred: Predecessors
    index: The index of the smallest path from the compPathlist
    tempIndex: The temporary next starting node for calculating the route to this node
    insertIndex: The Index at which point the new predecessor is inserted into the nodeList 
    '''
    @property
    def getNodeList(self):
        # If the starting point has a good, that needs to be picked up, pick it up.
        if self.bb_list[self.start - 1] == 1:
            self.bb_list[self.start - 1] = 0
        searchElement = 1

        # Write at the end of the bb_list a "2" to indicate the last node to visit on the list.
        self.bb_list[self.end - 1] = 2
        nodeList = [self.start]
        compPathList = []
        indexPathList = []
        startIndex = self.start

        # Loop fills the nodeList.
        while sum(self.bb_list) != 0:
            sPath, pred = Dijkstra.Dijkstra.dijkstra(self.graph, startIndex)
            # Looks at all next locations to visit and gets the distances between the current node and the next nodes
            # from the Dijkstra algorithm. Chooses the shortest path from the compPathList and saves it in the nodeList.
            for i, element in enumerate(sPath):
                if self.bb_list[i] == searchElement:
                    compPathList.append(element)
                    indexPathList.append(i)
            index = indexPathList[compPathList.index(min(compPathList))]
            self.bb_list[index] = 0
            nodeList.append(index + 1)

            # Get all the predecessors between the current node and the next node and put them into the nodeList.
            insertIndex = len(nodeList) - 1
            tempIndex = index
            while pred[tempIndex] != startIndex:
                nodeList.insert(insertIndex, pred[tempIndex])
                tempIndex = pred[tempIndex] - 1

            # Clear all comparison lists for the next loop and change the next starting node. Check, if all nodes have
            # been visited to assure the termination of the loop.
            compPathList.clear()
            indexPathList.clear()
            startIndex = index + 1
            if self.bb_list.count(1) == 0:
                searchElement = 2

        return nodeList

    '''
    Prints the list of nodes, their distances and the total distance.
    pathLengthList: Distances of all Nodes to the next one. There are n-1 distances in this list compared to the nodeList
    counter: Counter variable for the loop
    '''
    def outputSolution(self, nodeList):
        pathLengthList = []
        counter = 0
        while counter != len(nodeList) - 1:
            pathLengthList.append(self.getPathLength(nodeList[counter], nodeList[counter + 1]))
            counter += 1

        # Print Solution
        print("nodeList:        ", nodeList)
        print("pathLengthList:  ", pathLengthList)
        print("Total distance:  ", round(sum(pathLengthList), 3))
        return

    '''
    Calculates the path-length between two nodes.
    x: x-position
    y: y-position and distance
    node: y-position
    path-length: distance
    '''
    def getPathLength(self, startNode, endNode):
        for x, y in self.graph.items():
            for node, pathLength in y:
                if node == endNode and x == startNode:
                    return pathLength
        return 0

    '''
    Converts the list into a graph for the Dijkstra algorithm.
    graphDic: Graph to save the data
    i: index
    neighbour: List of neighbours
    templist: List of neighbours for one node
    '''
    def convertToGraph(self):
        graphDic = {}
        for i, neighbour in enumerate(self.neighbours):
            tempList = []
            for element in neighbour:
                tempList.append((element, round(math.dist(self.coordinates[i], self.coordinates[element - 1]), 3)))

            graphDic[i + 1] = tempList
        return graphDic

'''
Main function to run the Path_Finder
'''
if __name__ == '__main__':

    pf = Path_Finder(6, 7, "rtp_0_7.txt")
    pf.createRoute()
