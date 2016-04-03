import wizards.my_queue

def heuristic(a,b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def heuristic_diagonal(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return 1 * (dx + dy) + (1 - 2 * 1) * min(dx, dy)

def a_star_search(graph, start, goal):
    
    frontier = wizards.my_queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbours(current):
            new_cost = cost_so_far[current] + 1 #graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_diagonal(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
                
    
    #return came_from, cost_so_far
    p = reconstruct_path(came_from, start, goal)
    return p

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
    