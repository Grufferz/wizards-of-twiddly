

class SquareGrid:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.walls = []

    def cost(self):
        return 1

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbours(self, id):
        (x, y) = id

        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y-1), (x-1, y+1)]

        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)

        return results

class SquareGrid2:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.walls = []

    def cost(self):
        return 1

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbours(self, id):
        (x, y) = id

        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]

        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)

        return results

    
        