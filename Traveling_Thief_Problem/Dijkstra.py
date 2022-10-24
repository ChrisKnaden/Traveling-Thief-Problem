import math
import queue as Q

'''
Class for the Dijkstra algortihm
'''
class Dijkstra(object):

    def dijkstra(graph, s=1):
        # Get |V|
        n = len(graph)

        # Next we initialize predecessor list, list of distances to each node
        # and a list indicating for each node whether it is already visited
        # Note, that we add a dummy element each (the element at position 0),
        # in order to avoid pesky addition of 1 (since our node numbering starts at 1)
        n2 = n + 1
        preds = [-1] * n2
        dists = [math.inf] * n2
        done = [False] * n2

        preds[s] = s
        dists[s] = 0
        queue = Q.PriorityQueue()
        queue.put((dists[s], s))

        while not queue.empty():
            # Unpack next node
            dv, v = queue.get()
            done[v] = True
            # Now iterate over all neighbours. Note that we unpack the node number w and weight of edge (v,w)
            for w, dvw in graph[v]:
                # Nothing to do if shortest path already found
                if done[w]:
                    continue
                # Eventually update distance and predecessor
                if (dists[v] + dvw < dists[w]):
                    dists[w], preds[w] = dists[v] + dvw, v
                # Add node to priority queue
                queue.put((dists[w], w))

        return ((dists[1:], preds[1:]))
