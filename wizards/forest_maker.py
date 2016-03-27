import pygame
import wizards.constants, random, math, wizards.forest_loader


class Point():
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        self.cur_cov = 0
      
      
class Range():
    
    def __init__(self,p1,p2):
        self.pt1 = p1
        self.pt2 = p2
      


class ForestMaker(object):
    
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.forest = []
        self.forest = [[0 for x in range(w)] for y in range(h)]
        
        self.trees = []

        self.seeds = {}   
        
        self.fin = False
        
        self.collision_map = []
        self.collision_map = [[0 for x in range(wizards.constants.WIDTH)] for y in range(wizards.constants.HEIGHT)]
    
    def add_tree(self,x,y):
        
        self.forest[y][x] = 1
        p = Point(x,y)
        self.trees.append(p)    
        
        xp = int((x*wizards.constants.F_BLOCKS) / wizards.constants.CHAR_SIZE)
        yp = int((y*wizards.constants.F_BLOCKS) / wizards.constants.CHAR_SIZE)
        self.collision_map[yp][xp] = 1         
        

    def get_coverage(self):
        
        size = self.width * self.height
        counter = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.forest[y][x] == 1:
                    counter += 1
                    
        return counter / size
    
    def is_valid(self,x,y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height
    
    def find_range(self,x,y,rad):
        
        l = []
        
        if self.is_valid(x,y):
            
            minim = max(0, x-rad)
            maxim = min(self.width-1, x+rad)
            
            l.append(Range(Point(minim,y), Point(maxim,y)))
            
            for i in range(rad+1):
                r = int(math.sqrt(rad*rad - i*i))
                if y-i >= 0:
                    minim = max(0,x-r)
                    maxim = min(self.width-1,x+r)
                    l.append(Range(Point(minim,y-i), Point(maxim,y-i)))
                    
                if y+i < self.height:
                    minim = max(0,x-r)
                    maxim = min(self.width-1,x+r)
                    l.append(Range(Point(minim,y+i), Point(maxim,y+i)))                
            
        return l
    
    def remove_seeds(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.forest[y][x] == 2:
                    self.forest[y][x] = 0         
    
    def seed_trees(self):
        
        for p in self.trees:
            ranges = self.find_range(p.x,p.y,wizards.constants.SEED_RADIUS)
            
            for r in ranges:
                point1 = r.pt1
                point2 = r.pt2
                beg = int(point1.x)
                end = int(point2.x) + 1
                
                
                for x in range(beg, end):
                    if self.forest[point1.y][x] == 1:
                        continue
                    
                    self.forest[point1.y][x] == 2
                    seed_key = str(x) + "," + str(point1.y)
                    v = self.seeds.get(seed_key)
                    if v is None:
                        v = 0.0
                    self.seeds[seed_key] = v + wizards.constants.SEED_STRENGTH
                    
                    
    def step(self):
        #global seeds
        #decay existing seeds
        temp = {}
        if len(self.seeds) > 0:
            for k,v in self.seeds.items():
                temp[k] = v - (wizards.constants.SEED_DECAY*v)
                
        self.seeds = temp.copy()
        
        #create new trees
        for s in self.seeds:
            v = self.seeds[s]
            if random.random() < v:
                tokens = s.split(",")
                #print(tokens[0] + " " + tokens[1])
                self.add_tree(int(tokens[0]),int(tokens[1]))
        

        #remove seeds if tree is there
        for p in self.trees:
            k = str(p.x) + "," + str(p.y)
            if k in self.seeds:
                del self.seeds[k]
                
        #seed trees
        self.seed_trees()
        
    
    def create_forest(self):
        
        for i in range(wizards.constants.INIT_TREES):
            x = random.randrange(2, self.width-2)
            y = random.randrange(2, self.height-2)
            
            while self.forest[y][x] == 1:
                x = random.randrange(2, self.width-2)
                y = random.randrange(2, self.height-2)  
            
            self.add_tree(x,y)
            
        #seed_trees()
        cur_cov = self.get_coverage()
        
        while cur_cov < wizards.constants.DES_COVERAGE:
            self.step()
            cur_cov = self.get_coverage()
            
        self.remove_seeds()
        
        return self.forest
    
    def create_basic_forest(self):
        
        for i in range(wizards.constants.INIT_TREES):
            x = random.randrange(2, self.width-2)
            y = random.randrange(2, self.height-2)  
            
            while self.forest[y][x] == 1:
                x = random.randrange(2, self.width-2)
                y = random.randrange(2, self.height-2)   
            
            self.add_tree(x,y)      
            
    def update_forest_progress(self):
        
        self.cur_cov = self.get_coverage()
        
        if self.cur_cov < wizards.constants.DES_COVERAGE:
            self.step()
            self.cur_cov = self.get_coverage()   
        else:
            self.remove_seeds()
            self.fin = True

        fl = wizards.forest_loader.ForestLoader(self.cur_cov, self.fin)
        return fl
    
    def return_finished_forest(self):
        return self.forest
    
    def return_coll_map(self):
        return self.collision_map