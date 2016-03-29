import pygame, random
import wizards.building_maker, wizards.forest_maker, wizards.game_objects, wizards.my_queue, wizards.game_screen
class LoadingScreen(object):
    
    def __init__(self,level):
        super(LoadingScreen, self).__init__()
        random.seed(wizards.constants.NOW)
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)

        global now
        print(str(wizards.constants.NOW))
        self.bm = wizards.building_maker.BuildingsMaker(wizards.constants.WIDTH,wizards.constants.HEIGHT)
        self.bm.build_map(wizards.constants.BUILDINGS)
        self.buildings = None
        self.buildings_loaded = False
        self.level = level
        
        #self.fm = forest_maker.ForestMaker(constants.GLOBAL_W,constants.GLOBAL_H)
        self.fm = wizards.forest_maker.ForestMaker(wizards.constants.FWIDTH,wizards.constants.FHEIGHT)
        self.fm.create_basic_forest()
        self.world = None
        self.c_map = None
        self.f_count = 0
        self.finished = False
        
        self.ob_started = False
        self.object_map = []
        self.objects_loaded = False
        self.c = 0
        
        self.regions_loaded = False
        self.regions_started = False
        self.region_map = [[0 for x in range(wizards.constants.WIDTH)] for y in range(wizards.constants.HEIGHT)]
        self.total_regions = 0   
        self.largest_region = 0
        self.max_region = 0
        
        #self.treasure_map = [[0 for x in range(constants.WIDTH)] for y in range(constants.HEIGHT)]
        self.treasure_locations = None
        self.pl_start = None
        self.special_zones = []
           
        

        
    def render(self, screen):
        screen.fill(wizards.constants.BLACK)
        text5 = self.font.render('Loading Level ' + str(self.level), True, wizards.constants.WHITE)
        text1 = self.font.render('Loading Map: ' + str(self.f_count) + "%", True, wizards.constants.WHITE)
        
        text2 = self.sfont.render('Press SPACE', True, wizards.constants.WHITE)
        screen.blit(text5, (400,100))
        screen.blit(text1, (400,200))
        if self.finished:
            o_l_p = int((self.c / wizards.constants.FHEIGHT) * 100)
            text3 = self.sfont.render('Loading Objects: ' + str(o_l_p) + "%", True, wizards.constants.WHITE)
            screen.blit(text3, (400,300))
        if self.finished and self.objects_loaded:
            text4 = self.sfont.render('Processing Map', True, wizards.constants.WHITE)
            screen.blit(text4, (400,400))
        if self.finished and self.objects_loaded and self.regions_loaded:
            screen.blit(text2, (400,550))
    
    def update(self):
        if not self.buildings_loaded:
            self.buildings = self.bm.return_buildings()
            self.buildings_loaded = True
        if not self.finished:
            fl = self.fm.update_forest_progress()
            self.f_count =  min(int((fl.coverage / wizards.constants.DES_COVERAGE)), 100)
            if fl.fin:
                self.finished = True
                self.world = self.fm.return_finished_forest()
                self.create_collision_map()
                self.setup_objects()
                self.ob_started = True
                
        if self.ob_started and self.finished:
            if self.c < wizards.constants.FHEIGHT:
                self.populate_objects(self.c)
                self.c += 1
            else:
                self.objects_loaded = True
                
        if self.ob_started and self.finished and not self.regions_loaded:
            self.max_region = self.process_regions()  
            self.regions_loaded = True
            self.treasure_locations = self.wall_test()
            self.pl_start = self.get_player_start()
            #self.special_zones += self.carve_exit()

            self.special_zones = self.carve_door(self.pl_start[0], self.pl_start[1])
            self.special_zones += self.carve_exit()
            # self.print_map(self.c_map)
                
    def handle_events(self, events):
        for e in events:
            if self.finished and self.objects_loaded and self.regions_loaded:
                if e.type == pygame.KEYDOWN:
                    self.manager.go_to(wizards.game_screen.GameScreen(self.world, self.c_map, self.object_map, self.region_map, self.total_regions,
                                                                      self.max_region, self.buildings, self.treasure_locations, self.level,
                                                                      self.pl_start, self.special_zones))
                    
    
    
    def create_collision_map(self):

        self.c_map = self.fm.return_coll_map()        

        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.buildings[y][x] == 1:
                    self.c_map[y][x] = 1       
        
        
    def populate_objects(self, column):
        #for y in range(constants.FHEIGHT):
        for x in range(wizards.constants.FWIDTH):
            if self.world[column][x] == 1:
                # TODO optimise the fire effect grid
                f = wizards.game_objects.FireEffect(25.0)
                self.object_map[column][x] = wizards.game_objects.TreeWood(x,column,f)
                    
    def setup_objects(self):
        blank_obj = wizards.game_objects.BlankObject()
        self.object_map = [[blank_obj for x in range(wizards.constants.FWIDTH)] for y in range(wizards.constants.FHEIGHT)]
        
        
    def get_walls(self):
        retlist = []
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.c_map[y][x] == 1:
                    t = (x, y)
                    retlist.append(t)   
        return retlist
    
    def count_wall_neighbours(self, x, y):
        count = 0
        if self.is_valid_square(x,y-1):
            if self.buildings[y-1][x] == 1:
                count += 1
        if self.is_valid_square(x,y+1):
            if self.buildings[y+1][x] == 1:
                count += 1 
        if self.is_valid_square(x-1,y):
            if self.buildings[y][x-1] == 1:
                count += 1   
        if self.is_valid_square(x+1,y):
            if self.buildings[y][x+1] == 1:
                count += 1            
        return count
        
    def wall_test(self):
        #count = 0
        #threes = []
        twos = []
        for y in range(2,wizards.constants.HEIGHT-2):
            for x in range(2,wizards.constants.WIDTH-2):
                #if self.count_wall_neighbours(x,y) == 3:
                    #tup = (x,y)
                    #threes.append(tup)
                    #count += 1
                if self.c_map[y][x] == 0:
                    if self.count_wall_neighbours(x,y) >= 2:
                        tup = (x,y)
                        twos.append(tup)
        return twos
        
    def is_valid_square(self,x,y):
        return 0 <= x < wizards.constants.WIDTH and 0 <= y < wizards.constants.HEIGHT
                    
    def setup_graph(self):
        retlist = []
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                pass
    
    def process_regions(self):
        grid = wizards.square_grid.SquareGrid(wizards.constants.WIDTH,wizards.constants.HEIGHT)
        grid.walls = self.get_walls()
        self.total_regions += 1
        max_count = 0
        largest = 0
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.region_map[y][x] == 0 and self.c_map[y][x] == 0:
                    self.region_map[y][x] = self.total_regions
                    start = (x,y)
                    size_region = self.set_regions(grid, start, self.total_regions)
                    if size_region > largest:
                        largest = size_region
                        max_count = self.total_regions
                    self.total_regions += 1
        #self.print_map(self.region_map)        
        return max_count
        

    def set_regions(self, graph, start, cur_reg):
        frontier = wizards.my_queue.MyQueue()
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

    def get_player_start(self):
        l = []
        y = wizards.constants.HEIGHT - 2
        for x in range(3, wizards.constants.WIDTH - 3):
            if self.c_map[y][x] == 0:
                if self.get_cur_region(x,y) == self.max_region:
                    tup = (x,y)
                    l.append(tup)

        if len(l) > 0:
            t = random.choice(l)
            return t
        else:
            return (0,0)

    def get_cur_region(self, x, y):
        return self.region_map[y][x]

    def in_largest_region(self,x,y):
        return self.region_map[y][x] == self.largest_region

    def carve_door(self, x, y):
        ret_list = []

        self.c_map[y+1][x] = 0
        self.c_map[y+1][x-1] = 0
        self.c_map[y+1][x+1] = 0
        self.c_map[y+1][x-2] = 0
        self.c_map[y+1][x+2] = 0

        self.buildings[y + 1][x] = 0
        self.buildings[y + 1][x - 1] = 0
        self.buildings[y + 1][x + 1] = 0
        self.buildings[y + 1][x - 2] = 0
        self.buildings[y + 1][x + 2] = 0

        ret_list.append((y+1, x))
        ret_list.append((y+1, x-1))
        ret_list.append((y+1, x-2))
        ret_list.append((y+1, x+1))
        ret_list.append((y+1, x+2))

        return ret_list

    def carve_exit(self):
        ret_list = []
        l = []
        y = 1
        for x in range(4, wizards.constants.WIDTH - 4):
            if self.c_map[y][x] == 0:
                if self.get_cur_region(x,y) == self.max_region:
                    tup = (x,y)
                    l.append(tup)

        t = random.choice(l)
        xp = t[0]
        yp = t[1]

        self.c_map[yp-1][xp] = 0
        self.c_map[yp-1][xp+1] = 0
        self.c_map[yp-1][xp-1] = 0
        self.c_map[yp-1][xp-2] = 0
        self.c_map[yp-1][xp+2] = 0

        self.buildings[yp-1][xp] = 0
        self.buildings[yp-1][xp+1] = 0
        self.buildings[yp-1][xp-1] = 0
        self.buildings[yp-1][xp-2] = 0
        self.buildings[yp-1][xp+2] = 0

        ret_list.append((yp-1, xp+2))
        ret_list.append((yp-1, xp+1))
        ret_list.append((yp-1, xp))
        ret_list.append((yp-1, xp-1))
        ret_list.append((yp-1, xp-2))

        return ret_list

    def print_map(self, m):
        s = ""
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                s += str(m[y][x])
            s += "\n"
        print(s)    
            
        