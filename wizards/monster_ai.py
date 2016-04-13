import random, time
import wizards.square_grid, wizards.constants, wizards.searches, wizards.utils, wizards.light_map, wizards.resolve_combat

class BasicAI():

    def __init__(self, coll_map):
        self.memory = None
        self.sg = None
        self.view_distance = 20
        self.los = 30
        self.collision_map = coll_map
        self.light = wizards.light_map.LightMap(self.collision_map)

    def update(self, monster, player, player_map, collision_map, monster_map, combat_resolver):
        pass

    def is_lit(self,x,y):
        return self.light.lit(x,y)

    def is_valid_move(self, pos_tup, map):
        return pos_tup in map

    def find_lowest_neighbour(self, monster, check_map, monster_map, player, memory=False):
        if memory:
            mons_x = 20
            mons_y = 20
        else:
            mons_x = monster.x
            mons_y = monster.y
        neighbours = [(mons_x - 1, mons_y), (mons_x + 1, mons_y),
                      (mons_x, mons_y + 1), (mons_x, mons_y - 1),
                      (mons_x + 1, mons_y + 1), (mons_x + 1, mons_y - 1),
                      (mons_x - 1, mons_y + 1), (mons_x - 1, mons_y - 1)
                      ]
        possible_moves = []
        lowest = 999
        if (20,20) in check_map:
            cur_value = check_map[(mons_x, mons_y)]
        else:
            cur_value = 999
        print("CV=" + str(cur_value))
        for n in neighbours:
            if self.is_valid_move(n, check_map):
                if check_map[n] <= cur_value:
                    if check_map[n] <= lowest:
                        lowest = check_map[n]
        print("LOWEST=" + str(lowest))
        if lowest == 999:
            return None
        else:
            for n in neighbours:
                if n in check_map:
                    if check_map[n] == lowest:
                        possible_moves.append(n)
            return possible_moves

    def find_highest_neighbour(self, monster, check_map, monster_map, player, memory=False):
        if memory:
            mons_x = 20
            mons_y = 20
        else:
            mons_x = monster.x
            mons_y = monster.y
        neighbours = [(mons_x - 1, mons_y), (mons_x + 1, mons_y),
                      (mons_x, mons_y + 1), (mons_x, mons_y - 1),
                      (mons_x + 1, mons_y + 1), (mons_x + 1, mons_y - 1),
                      (mons_x - 1, mons_y + 1), (mons_x - 1, mons_y - 1)
                      ]
        possible_moves = []
        highest = 0
        if (20, 20) in check_map:
            cur_value = check_map[(mons_x, mons_y)]
        else:
            cur_value = 0
        print("CV=" + str(cur_value))
        for n in neighbours:
            if self.is_valid_move(n, check_map):
                if check_map[n] > cur_value:
                    if check_map[n] > highest:
                        highest = check_map[n]
        if highest == 0:
            return None
        else:
            for n in neighbours:
                if n in check_map:
                    if check_map[n] == highest:
                        possible_moves.append(n)
            return possible_moves

    def check_other_monsters(self, pos_tup, monster_map):
        return pos_tup in monster_map

    def set_up_memory(self, monster, player, collision_map, mons_list):

        self.sg = wizards.square_grid.SquareGrid2(40, 40)
        self.sg.walls = self.setup_walls(collision_map, monster, mons_list)
        #print_walls(self.sg.walls)#

        px = abs(monster.x -  player.x)
        py = abs(monster.y - player.y)
        if monster.x > player.x:
            px = self.view_distance - px
        elif monster.x <= player.x:
            px = self.view_distance + px
        if monster.y > player.y:
            py = self.view_distance - py
        elif monster.y <= player.y:
            py = self.view_distance + py
        target = (px, py)
        print(str(monster.x) + "__" + str(monster.y))
        print(str(player.x) + "__" + str(player.y))
        print(str(px) + "__" + str(py))
        print(str(heuristic_diagonal((player.x,player.y), (monster.x,monster.y))))
        #print_walls(self.sg.walls)
        self.memory = wizards.searches.breadth_first_search(self.sg, target)
        #if (20,20) in self.memory:
            #print(str(self.memory[(20, 20)]))

    def setup_walls(self, collision_map, monster, mons_list):
        first_pos_x = monster.x - self.view_distance
        first_pos_y = monster.y - self.view_distance
        last_pos_x = monster.x + self.view_distance
        last_pos_y = monster.y + self.view_distance
        walls = []
        local_x = 0
        local_y = 0
        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                # print(str(y) + "_" + str(x) + " >> " + str(local_y) + "_" + str(local_x))
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                    if (x,y) in mons_list:
                        walls.append((local_x, local_y))
                local_x += 1
            local_x = 0
            local_y += 1
        return walls


class ExploreAI(BasicAI):

    def __init__(self, collision_map):
        super().__init__(collision_map)
        self.sg = wizards.square_grid.SquareGrid2(20, 20)
        self.vd = 10

    def update(self,  monster, player, player_map, collision_map, monster_map, combat_resolver):

        start_time = time.time()

        self.sg.walls = self.setup_walls(collision_map, monster_map, monster)

        self.light.do_fov(monster.x, monster.y, self.los)

        targets = []
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.is_lit(x, y):
                    monster.level_seen[(x,y)] = 1

        first_pos_x = monster.x - self.vd
        first_pos_y = monster.y - self.vd
        last_pos_x = monster.x + self.vd
        last_pos_y = monster.y + self.vd
        local_x = 0
        local_y = 0
        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                # print(str(y) + "_" + str(x) + " >> " + str(local_y) + "_" + str(local_x))
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    continue
                else:
                    if (x, y) not in monster.level_seen:
                        targets.append((local_x,local_y))
                local_x += 1
            local_x = 0
            local_y += 1
        #print(str(targets))
        self.memory = wizards.searches.breadth_first_search_multi(self.sg, targets)

        print_wide_memory(self.memory)

        next_moves = self.find_lowest_neighbour(monster, self.memory, monster_map, player, True)

        if next_moves is not None:
            nm = random.choice(next_moves)
            print("NEXTMOVE=" + str(nm))
            x_mod = nm[0] - self.vd
            y_mod = nm[1] - self.vd

            monster.set_position(monster.x + x_mod, monster.y + y_mod, monster_map)
        else:
            print("NO MOVE!")



        print("UPDATE %s seconds --- " % (time.time() - start_time))

    def find_highest_neighbour(self, monster, check_map, monster_map, player, memory=False):
        if memory:
            mons_x = self.vd
            mons_y = self.vd
        else:
            mons_x = monster.x
            mons_y = monster.y
        neighbours = [(mons_x - 1, mons_y), (mons_x + 1, mons_y),
                      (mons_x, mons_y + 1), (mons_x, mons_y - 1),
                      (mons_x + 1, mons_y + 1), (mons_x + 1, mons_y - 1),
                      (mons_x - 1, mons_y + 1), (mons_x - 1, mons_y - 1)
                      ]
        possible_moves = []
        highest = 0
        if (self.vd, self.vd) in check_map:
            cur_value = check_map[(mons_x, mons_y)]
        else:
            cur_value = 0
        print("CV=" + str(cur_value))
        for n in neighbours:
            if self.is_valid_move(n, check_map):
                if check_map[n] > cur_value:
                    if check_map[n] > highest:
                        highest = check_map[n]
        if highest == 0:
            return None
        else:
            for n in neighbours:
                if n in check_map:
                    if check_map[n] == highest:
                        possible_moves.append(n)
            return possible_moves

    def find_lowest_neighbour(self, monster, check_map, monster_map, player, memory=False):
        if memory:
            mons_x = self.vd
            mons_y = self.vd
        else:
            mons_x = monster.x
            mons_y = monster.y
        neighbours = [(mons_x - 1, mons_y), (mons_x + 1, mons_y),
                      (mons_x, mons_y + 1), (mons_x, mons_y - 1),
                      (mons_x + 1, mons_y + 1), (mons_x + 1, mons_y - 1),
                      (mons_x - 1, mons_y + 1), (mons_x - 1, mons_y - 1)
                      ]
        possible_moves = []
        highest = 999
        if (self.vd, self.vd) in check_map:
            cur_value = check_map[(mons_x, mons_y)]
        else:
            cur_value = 999
        print("CV=" + str(cur_value))
        for n in neighbours:
            if self.is_valid_move(n, check_map):
                if check_map[n] <= cur_value:
                    if check_map[n] <= highest:
                        highest = check_map[n]
        if highest == 999:
            return None
        else:
            for n in neighbours:
                if n in check_map:
                    if check_map[n] == highest:
                        possible_moves.append(n)
            return possible_moves

    def setup_walls(self, collision_map, monster_map, monster):
        walls = []

        first_pos_x = monster.x - self.vd
        first_pos_y = monster.y - self.vd
        last_pos_x = monster.x + self.vd
        last_pos_y = monster.y + self.vd
        local_x = 0
        local_y = 0

        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                    #if (x,y) in monster_map:
                    #    walls.append((x,y))
                local_x += 1
            local_y += 1
            local_x = 0
        return walls


class AggressiveAI(BasicAI):

    def __init__(self, coll_map):
        super().__init__(coll_map)
        self.sg = wizards.square_grid.SquareGrid2(40, 40)
        self.vd = 20

    def __str__(self):
        return "Aggressive AI"

    def update(self, monster, player, player_map, collision_map, monster_map, combat_resolver):
        start_time = time.time()
        self.light.do_fov(monster.x, monster.y, self.los)

        w = self.setup_walls(collision_map, monster, monster_map)
        self.sg.walls= w

        dist_to_player = heuristic_diagonal((monster.x, monster.y), (player.x, player.y))
        print("DIST=" + str(dist_to_player))

        if dist_to_player < 2:
            print("FIGHT!")
            dmg = combat_resolver.monster_hit_player(monster, player)
        else:

            plx = (player.x - monster.x) + self.vd
            ply = (player.y - monster.y) + self.vd
            player_local = (plx, ply)

            n = self.get_neighbours(plx, ply)
            n = filter(self.passable, n)
            #n = filter(self.in_bounds, n)

            self.memory = wizards.searches.breadth_first_search_multi(self.sg, n)

            if (self.vd, self.vd) in self.memory:
                cur = self.memory[(self.vd, self.vd)]
                print("CURRENT SQUARE = " + str(cur))

                lowest_neighbours = self.find_lowest_neighbour(monster, self.memory, monster_map, player, True)
                if len(lowest_neighbours) > 0:
                    next_square = random.choice(lowest_neighbours)

                    print("NEXTMOVE=" + str(next_square))
                    x_mod = next_square[0] - self.vd
                    y_mod = next_square[1] - self.vd

                    monster.set_position(monster.x + x_mod, monster.y + y_mod, monster_map)
                else:
                    print("NO LOWEST NEIGHBOUR...")

            dmg = 0

        self.print_memory(self.memory)

        print("UPDATE AGGRESSIVE %s seconds --- " % (time.time() - start_time))

        return dmg

    def passable(self, id):
        return id not in self.sg.walls

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.vd and 0 <= y < self.vd

    def get_neighbours(self, xpos, ypos):
        neighbours = [(xpos - 1, ypos), (xpos + 1, ypos),
                      (xpos, ypos + 1), (xpos, ypos - 1),
                      (xpos + 1, ypos + 1), (xpos + 1, ypos - 1),
                      (xpos - 1, ypos + 1), (xpos - 1, ypos - 1), (xpos, ypos)
                      ]
        return neighbours

    def find_lowest_neighbour(self, monster, check_map, monster_map, player, memory=False):
        if memory:
            mons_x = self.vd
            mons_y = self.vd
        else:
            mons_x = monster.x
            mons_y = monster.y
        neighbours = [(mons_x - 1, mons_y), (mons_x + 1, mons_y),
                      (mons_x, mons_y + 1), (mons_x, mons_y - 1),
                      (mons_x + 1, mons_y + 1), (mons_x + 1, mons_y - 1),
                      (mons_x - 1, mons_y + 1), (mons_x - 1, mons_y - 1)
                      ]
        possible_moves = []
        highest = 999
        if (self.vd, self.vd) in check_map:
            cur_value = check_map[(mons_x, mons_y)]
        else:
            cur_value = 999
        print("CV=" + str(cur_value))
        for n in neighbours:
            if self.is_valid_move(n, check_map):
                if check_map[n] <= cur_value:
                    if check_map[n] <= highest:
                        highest = check_map[n]
        if highest == 999:
            return None
        else:
            for n in neighbours:
                if n in check_map:
                    if check_map[n] == highest:
                        possible_moves.append(n)
            return possible_moves

    def setup_walls(self, collision_map, monster_map, monster):

        walls = []

        first_pos_x = monster.x - self.vd
        first_pos_y = monster.y - self.vd
        last_pos_x = monster.x + self.vd
        last_pos_y = monster.y + self.vd
        local_x = 0
        local_y = 0

        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                    if (x,y) in monster_map:
                        walls.append((local_x, local_y))
                local_x += 1
            local_y += 1
            local_x = 0
        return walls

    def setup_walls(self, collision_map, monster, mons_list):
        first_pos_x = monster.x - self.view_distance
        first_pos_y = monster.y - self.view_distance
        last_pos_x = monster.x + self.view_distance
        last_pos_y = monster.y + self.view_distance
        walls = []
        local_x = 0
        local_y = 0
        m_list_to_add = []
        for m in mons_list:
            if m[0] != monster.x and m[1] != monster.y:
                #print(str(m))
                m_list_to_add.append(m)
        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                # print(str(y) + "_" + str(x) + " >> " + str(local_y) + "_" + str(local_x))
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                    if (x,y) in m_list_to_add:
                        walls.append((local_x, local_y))
                local_x += 1
            local_x = 0
            local_y += 1
        return walls

    def print_memory(self, m):
        s = ""
        for y in range(self.vd*2):
            for x in range(self.vd*2):
                if (x, y) in m:
                    v = m[(x, y)]
                    s += ('{0:04d}'.format(v))
                    s += " "
                else:
                    s += "XXXX "
            s += "\n"
        print(s)


class PassiveAI(BasicAI):

    def __init__(self, coll_map):
        super().__init__(coll_map)
        self.sg = wizards.square_grid.SquareGrid2(40, 40)
        self.vd = 20
        self.player_seen = False

    def __str__(self):
        return "Passive AI"

    def update(self, monster, player, player_map, collision_map, monster_map, combat_resolver):
        start_time = time.time()
        #print("UPDATE" + str(monster.ai))
        self.light.do_fov(monster.x, monster.y, self.los)

        self.player_seen = False

        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.is_lit(x, y):
                    monster.level_seen[(x, y)] = 1
                    if x == player.x and y == player.y:
                        self.player_seen = True

        if self.player_seen:

            monster.player_seen = True

            self.sg.walls = self.setup_walls(collision_map, monster_map, monster)

            plx = (player.x - monster.x) + self.vd
            ply = (player.y - monster.y) + self.vd
            player_local = (plx, ply)
            print("PL=" + str(player_local))

            if player_local is not None:
                self.memory = wizards.searches.breadth_first_search(self.sg, (player_local))

                if (self.vd, self.vd) in self.memory:
                    print("CURRENT SQUARE = " + str(self.memory[(self.vd, self.vd)]))
                    new_ai = AggressiveAI(collision_map)
                    monster.set_ai(new_ai)

                self.print_wide_memory(self.memory)

        else:

            print(monster.name + " can't see player")

        print("UPDATE PASSIVE %s seconds --- " % (time.time() - start_time))

        return 0

    def print_wide_memory(self, m):
        s = ""
        for y in range(self.vd*2):
            for x in range(self.vd*2):
                if (x, y) in m:
                    v = m[(x, y)]
                    s += ('{0:04d}'.format(v))
                    s += " "
                else:
                    s += "XXXX "
            s += "\n"
        print(s)

    def setup_walls(self, collision_map, monster_map, monster):

        walls = []

        first_pos_x = monster.x - self.vd
        first_pos_y = monster.y - self.vd
        last_pos_x = monster.x + self.vd
        last_pos_y = monster.y + self.vd
        local_x = 0
        local_y = 0

        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                        # if (x,y) in monster_map:
                        #    walls.append((x,y))
                local_x += 1
            local_y += 1
            local_x = 0
        return walls


def path_blocked(path, map):
    for p in path:
        xp = p[0]
        yp = p[1]
        if map[yp][xp] == 1:
            return True
    return False


def heuristic_diagonal(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return 1 * (dx + dy) + (1 - 2 * 1) * min(dx, dy)


def process_flee_map(map):
    ret_dict = {}
    for key, value in map.items():
        ret_dict[key] = (value * -6) // 5
    return  ret_dict


def print_map(m):
    s = ""
    for y in range(40):
        for x in range(40):
            if (x, y) in m:
                v = m[(x, y)]
                s += ('{0:04d}'.format(v))
                s += " "
            else:
                s += "XXXX "
        s += "\n"
    print(s)


def print_walls(m):
    s = ""
    for y in range(40):
        for x in range(40):
            if (x, y) not in m:
                v = 0
                s += ('{0:04d}'.format(v))
                s += " "
            else:
                s += "XXXX "
        s += "\n"
    print(s)


def print_wide_memory(m):
    s = ""
    for y in range(20):
        for x in range(20):
            if (x, y) in m:
                v = m[(x, y)]
                s += ('{0:04d}'.format(v))
                s += " "
            else:
                s += "XXXX "
        s += "\n"
    print(s)