from queue import PriorityQueue
'''
Class for the Branch and Bound algorithm
'''
class Branch_Bound():
    '''
    items: List, that contains the (weight, value) of an object, that can be collected
    max_capacity: The maximum capacity, that the thief can lift, it's "k" of the .txt file
    ratioed_items: List of value/weight ratio of items [(value/weight, weight, value, itemNumber),...]
    final_solutions: Contains the upper limit (O), the lower limit (U) and the list of which nodes to visit
    initialSol: List that contains only "-1" to indicate, which nodes have to be checked
    '''
    def __init__(self, items, max_capacity, ratioed_items):
        self.items = items
        self.max_capacity = max_capacity
        self.ratioed_items = ratioed_items
        self.final_solutions = []
        self.initialSol = len(items)*[-1]

    """
    Computes the upper and lower bounds as well as the remaining capacity of a given (partial) solution, returned as
    tuple (O,U,k).
    """
    def computeBounds(self, in_solution, capacity):
        U = 0
        k = capacity
        solution = in_solution.copy()

        i = 0;
        while i < len(solution) and solution[i] >= 0:
            if solution[i] == 1:
                k -= self.items[i][0]  # Subtract item weight from capacity
                U += self.items[i][1]  # Add certain value of item
            if solution[i] >= 0:
                i += 1  # Increase i

        O = U  # Start value for O is U

        available_items = self.ratioed_items[i:len(self.items)]
        # Sort according to weight/value ratio
        available_items.sort(reverse=True)

        # Compute upper bound and fill up solution
        for item in available_items:
            if item[1] < k:
                solution[item[3]] = 1
                k -= item[1]
                O += item[2]
            elif k > 0:
                O += item[2] * (k / item[1])
                solution[item[3]] = k / item[2]
                k = 0
            else:
                solution[item[3]] = 0
        return ((U, O, k, solution))

    """
    Branch a solution and add the resulting partial results to the given priority queue.
    """
    def branch(self, solution, queue):
        try:
            pos = list(solution).index(-1, )
            sol1 = list(solution).copy()
            sol1[pos] = 1
            U, O, k, sol = self.computeBounds(sol1, self.max_capacity)
            if k >= 0:
                queue.put((-O, -U, sol1))

            sol2 = list(solution).copy()
            sol2[pos] = 0
            U, O, k, sol = self.computeBounds(sol2, self.max_capacity)
            if k >= 0:
                queue.put((-O, -U, sol2))

        except ValueError:
            print("No partial solution anymore.")

        return

    """
    Keep the given solution with O and U in a list, if it is not dominated by another.
    """
    def storeFinal(self, O, U, sol):
        include = True
        # Store which elements to remove (later on)
        removalList = []

        # Determine which elements to keep and which to remove
        for i in range(len(self.final_solutions)):
            if self.final_solutions[i][0] < O:
                # Register for removal
                removalList.append(i)
            elif self.final_solutions[i][0] > O:
                include = False

        # Remove from final solution list (backwards)
        for i in range(len(removalList) - 1, 0, -1):
            del self.final_solutions[removalList[i]]

        # Include solution, if applicable
        if include:
            self.final_solutions.append((O, U, sol))

        return

    """
    Apply the bounding to the current queue and remove all dominated (partial) solutions.
    """
    def bounding(self, queue):
        elemList = []
        largestU = 0

        # Store queue content and determine largest lower bound
        while not queue.empty():
            elem = queue.get()
            elemList.append(elem)
            if -elem[1] > largestU:
                largestU = -elem[1]

        # Consider final set for lower bound as well
        for elem in self.final_solutions:
            if elem[1] > largestU:
                largestU = elem[1]

        # Add all de-queued elements to the queue again, which cannot be excluded due to U > O
        dequeued = len(elemList)
        for elem in elemList:
            if -elem[0] >= largestU:
                queue.put(elem)
                dequeued -= 1

        return queue

    '''
    Execution of the Branch and Bound.
    '''
    def executeBB(self):
        # Compute ratio of value/weight for given instance, store together with index
        ratioed_items = []
        for i in range(len(self.items)):
            ratioed_items.append((self.items[i][1] / self.items[i][0], self.items[i][0], self.items[i][1], i))

        q = PriorityQueue(maxsize=0)
        U, O, k, sol = self.computeBounds(self.initialSol, self.max_capacity)

        # Put initial solution to queue
        q.put((-O, -U, self.initialSol))

        # Perform B&B, until the queue is empty
        while not q.empty():
            # Get front element from queue
            curr_element = q.get()
            cU, cO, cSol = curr_element

            # Check whether this is a final solution
            if cSol[len(cSol) - 1] > -1:
                # Yes: store it and try to exclude some other solutions
                self.storeFinal(-cO, -cU, cSol)
                self.bounding(q)

            else:
                # No: try to exclude some other solutions, then branching
                idx = cSol.index(-1)
                self.branch(cSol, q)
                self.bounding(q)

        for elem in self.final_solutions:
           continue

        # Only return the BB list with the elements that need to be collected
        return elem[2]

