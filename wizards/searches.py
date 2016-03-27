import wizards.constants

def breadth_first_search(graph, start):
    frontier = wizards.my_queue.MyQueue()
    frontier.put(start)
    distance = {}
    distance[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        for next in graph.neighbours(current):
            if next not in distance:
                #print(current)
                frontier.put(next)
                distance[next] = 1 + distance[current]
                
    return distance


def breadth_first_search_multi(graph, starts):
    frontier = wizards.my_queue.MyQueue()
    distance = {}
    visited = {}
    for start in starts:
        #print(start)
        frontier.put(start)
        distance[start] = 0
        visited[start] = True
    
    while not frontier.empty():
        current = frontier.get()
        for next in graph.neighbours(current):
            if next not in visited:
                frontier.put(next)
                distance[next] = 1 + distance[current]
                visited[next] = True
                
    return distance