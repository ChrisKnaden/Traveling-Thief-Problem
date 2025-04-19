'''
Class to read and interpret the nodes of the .txt files
'''
class ReadFile(object):
    '''
    items: List, that contains the (weight, value) of an object, that can be collected
    max_capacity: The maximum capacity, that the thief can lift, it's "k" of the .txt file
    ratioed_items: List of value/weight ratio of items [(value/weight, weight, value, itemNumber),...]
    coordinates: List, that contains every location (x,y) of each Node, in the same order as in the .txt file
    neighbours: List of neighbours of each Node [neighbour1, neighbour2...]
    maxNodes: Total amount of Nodes
    '''
    def __init__(self, filename):
        self.filename = filename

    global items
    global max_capacity
    global ratioed_items
    global coordinates
    global neighbours
    global maxNodes

    """
    Import an instance from file and overwrite the default global nodes. This method only reads the necessary nodes 
    information on weights and utility of objects as well as the maximum capacity of the knapsack (k). The method
    returns items, neighbours, coordinates, ratioed_items and max_capacity.
    fields: Each line of the .txt file is splitted by the blank character
    value_mode: After the information of the .txt file about max_capacity and maxNodes is collected, the boolean
                indicates to proceed with reading the node values.
    """
    def readInstance(self):
        value_mode = False
        file = open(self.filename)
        for line in file:
            fields = line.strip().split()
            if not value_mode and not fields[0] == "#EOF":
                if fields[0] == "k":
                    max_capacity = int(fields[2])
                elif fields[0] == "N":
                    maxNodes = int(fields[2])
                elif fields[0] == "#NODES":
                    value_mode = True
                    items = []
                    coordinates = []
                    neighbours = []

            elif not fields[0] == "#EOF":
                items.append(eval(fields[2]))
                coordinates.append(eval(fields[1]))
                # Try to add the neighbours. If there is no neighbour specified in the .txt file, add all potential
                # neigbhours.
                try:
                    neighbours.append(eval(fields[3]))
                except:
                    counter = 1
                    tempList = []
                    while counter <= maxNodes:
                        tempList.append(counter)
                        counter += 1
                    tempList.remove(eval(fields[0]))
                    neighbours.append(tempList)

        # Recompute ratios based on read values
        ratioed_items = []
        for i in range(len(items)):
            ratioed_items.append((items[i][1] / items[i][0], items[i][0], items[i][1], i))

        return items, neighbours, coordinates, ratioed_items, max_capacity