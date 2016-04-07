import random, time
import wizards.square_grid, wizards.constants, wizards.searches, wizards.utils

class BasicAI():

    def __init__(self):
        self.memory = None
        self.sg = None
        self.view_distance = 16

    def update(self, monster, player, player_map, collision_map, monster_map):
        start_time = time.time()
        dist_to_player = heuristic_diagonal((player.x, player.y), (monster.x, monster.y))
        print("Distance from " + monster.name + " to player = " + str(dist_to_player))

        if dist_to_player <= 40:
            line = wizards.utils.get_line((monster.x, monster.y), (player.x, player.y))
            print("LENNY LINE FOR " + monster.name + " = " + str(len(line)))

            if path_blocked(line, collision_map):
                print(monster.name + " can't see")
            else:
                print(monster.name + " sees player")

                if dist_to_player <= self.view_distance:
                    self.set_up_memory(monster, player, collision_map)
                    #if monster.monster_id < 2:
                    print_map(self.memory)

        neighbours = [(monster.x-1, monster.y), (monster.x+1, monster.y),
                      (monster.x, monster.y+1), (monster.x, monster.y-1),
                      (monster.x+1, monster.y + 1), (monster.x+1, monster.y - 1),
                      (monster.x-1, monster.y + 1), (monster.x-1, monster.y - 1)
                      ]

        possible_moves = []
        cur_value = player_map[(monster.x, monster.y)]
        for n in neighbours:
            if self.is_valid_move(n, player_map) and not self.check_other_monsters(n, monster_map):
                x = n[0]
                y = n[1]
                if player_map[n] < cur_value:
                    possible_moves.append(n)

        if len(possible_moves) > 0:
            next_move = random.choice(possible_moves)
            monster.set_position(next_move[0], next_move[1], monster_map)

        print("UPDATE %s seconds --- " % (time.time() - start_time))

    def is_valid_move(self, pos_tup, map):
        return pos_tup in map

    def check_other_monsters(self, pos_tup, monster_map):
        return pos_tup in monster_map

    def set_up_memory(self, monster, player, collision_map):

        first_pos_x = monster.x - self.view_distance
        first_pos_y = monster.y - self.view_distance
        last_pos_x = monster.x + self.view_distance
        last_pos_y = monster.y + self.view_distance

        self.sg = wizards.square_grid.SquareGrid2(32, 32)
        walls = []
        local_x = 0
        local_y = 0
        for y in range(first_pos_y, last_pos_y):
            for x in range(first_pos_x, last_pos_x):
                #print(str(y) + "_" + str(x) + " >> " + str(local_y) + "_" + str(local_x))
                if y < 0 or y >= wizards.constants.HEIGHT or x < 0 or x >= wizards.constants.WIDTH:
                    walls.append((local_x, local_y))
                else:
                    if collision_map[y][x] == 1:
                        walls.append((local_x, local_y))
                local_x += 1
            local_x = 0
            local_y += 1

        self.sg.walls = walls
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
        if (16,16) in self.memory:
            print(str(self.memory[(16, 16)]))


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
    for y in range(32):
        for x in range(32):
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
    for y in range(32):
        for x in range(32):
            if (x, y) not in m:
                v = 0
                s += ('{0:04d}'.format(v))
                s += " "
            else:
                s += "XXXX "
        s += "\n"
    print(s)