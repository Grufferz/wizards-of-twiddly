import random


class BuildingsMaker():
    
    def __init__(self, w, h):
        self.width = w
        self.height = h
        
        self.layout = []
        self.layout = [[0 for x in range(w)] for y in range(h)]  
        
        #self.region_map = [[0 for x in range(w)] for y in range(h)]  
        #self.total_regions = 0   
        #self.largest_region = 0
        #self.max_region = 0        
        
        self.des_coverage = 0.9
                      
           
    
    def get_coverage(self):
        size = self.width * self.height
        w = (self.width*2) + (self.height*2)
        counter = 0 - w
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == 1:
                    counter += 1
                    
        return counter / size
    
    def return_buildings(self):
        return self.layout
    
    def generate_walls(self):
        for x in range(self.width):
            self.layout[0][x] = 1
            self.layout[self.height-1][x] = 1
        for y in range(self.height):
            self.layout[y][0] = 1
            self.layout[y][self.width-1] = 1
            
    #phase 2
    
    def create_array(self, xsize, ysize, thick):
        arr = [[0 for x in range(xsize)] for y in range(ysize)]
        if thick < 50:
            for x in range(xsize):
                arr[0][x] = 1
            for y in range(ysize):
                arr[y][0] = 1
        else:
            for x in range(xsize):
                arr[0][x] = 1
                if ysize >= 1:
                    arr[1][x] = 1
            for y in range(ysize):
                arr[y][0] = 1    
                if xsize >= 1:
                    arr[y][1] = 1
        return arr
    
    
    def rotate_array(self, arr):
        output = []
        h = len(arr)
        w = len(arr[0])
        for row in range(w):
            newrow = []
            for col in range(h):
                newrow.append(arr[h - 1 - col][row])
            output.append(newrow)
        return output
    
    def build_map(self, desired):
        
        self.generate_walls()
        current = self.get_coverage()
        
        while current < desired:
            self.place_building()
            current = self.get_coverage()
            #print(str(current))
        
        #self.process_regions()

        #if self.total_regions > 1:
            #print("MORE")
    
    def place_building(self):
        
        arr_w = random.randrange(2, 8)
        arr_h = random.randrange(2, 8)

        #end_x = min(startx + arr_w, 
        #end_y = starty + arr_h
        #print(str(end_y) + "_" + str(end_x))

        arr = self.create_array(arr_w,arr_h, random.randrange(1,101))
        
        times_rotation = random.randrange(4)
        for i in range(times_rotation):
            arr = self.rotate_array(arr)
            
        startx = min(random.randrange(3, self.width - 3), self.width - len(arr[0]) - 4)
        starty = min(random.randrange(3, self.height - 3), self.height - len(arr) -4)            
            
        for y in range(len(arr)):
            for x in range(len(arr[0])):
                xp = x + startx
                yp = y + starty
                if arr[y][x] == 1:
                    self.layout[yp][xp] = 1

        
        #self.print_arr(arr)
        
        
    def get_walls(self):
        retlist = []
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == 1:
                    t = (x, y)
                    retlist.append(t)   
        return retlist        
        
    def process_regions(self):
        grid = square_grid.SquareGrid(self.width,self.height)
        grid.walls = self.get_walls()
        self.total_regions += 1
        max_count = 0
        largest = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.region_map[y][x] == 0 and self.layout[y][x] == 0:
                    self.region_map[y][x] = self.total_regions
                    start = (x,y)
                    size_region = self.set_regions(grid, start, self.total_regions)
                    if size_region > largest:
                        largest = size_region
                        max_count = self.total_regions
                    self.total_regions += 1
        self.print_arr(self.region_map)        
        return max_count    
        
    def set_regions(self, graph, start, cur_reg):
        frontier = my_queue.MyQueue()
        frontier.put(start)
        came_from = {}
        came_from[start] = None
    
        while not frontier.empty():
            current = frontier.get()
            for next in graph.neighbours(current):
                if next not in came_from:
                    xp = next[0]
                    yp = next[1]
                    self.region_map[yp][xp] = cur_reg
                    frontier.put(next)
                    came_from[next] = current
                    
        return len(came_from)
        
    
    def print_arr(self, a):
        s = ""
        for y in range(len(a)):
            for x in range(len(a[0])):
                s += str(a[y][x])
            s += "\n"        
        print(s)
        
    def print_map(self):
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                s += str(self.layout[y][x])
            s += "\n"
            
        s += "\n"
        s += "\n"
        print(s)    
        
        
#b = BuildingsMaker(160,82)
##a = b.create_array(12,5)
#b.build_map(0.1)
#b.print_map()
##t = b.process_regions()