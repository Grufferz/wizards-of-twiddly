import pygame, random
import wizards.constants, wizards.monster_ai

class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__()
        self.monster_id = mid
        self.x = x
        self.y = y        
        self.name = name
        self.level = level
        self.orig_hp = self.get_hp(level)
        self.hp = self.orig_hp  
        self.dead = False
        self.weapon = None
        self.current_weapon = None
        self.m_type = m_type
        self.fleeing = False
        self.morale = 6
        self.save_magic = 16
        self.undead = False
        self.never_surrender = False

        self.weight = 0

        self.charmable = True
        self.charmed = False
        self.charmed_by = None
        self.charm_duration = 0
        self.charm_gfx = None

        self.asleep = False
        self.asleep_for = 0

        # TODO Monster AI
        self.ai = wizards.monster_ai.BasicAI()
        self.moved = False

    def get_id(self):
        return self.monster_id
        
    def updatePosition(self,direction,col_map):
        
        new_x = self.x
        new_y = self.y
        if direction == 0:
            new_y = self.y - 1
        elif direction == 1:
            new_x = self.x + 1
        elif direction == 2:
            new_y = self.y + 1
        elif direction == 3:
            new_x = self.x - 1  
        
        if self.is_valid_move(new_x, new_y, col_map):
            self.x = new_x
            self.y = new_y
            
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def __str__(self):
        return self.name + ": " + str(self.monster_id) + " >> "+ str(self.y) + "_" + str(self.x)

    def __eq__(self, other):
        return self.monster_id == other.monster_id

    def __lt__(self, other):
        return self.monster_id < other.monster_id

    def __hash__(self):
        return self.monster_id

    def set_position(self, x, y, monster_map):

        if (self.x, self.y) in monster_map:
            del monster_map[(self.x, self.y)]

        self.x = x
        self.y = y
        monster_map[(self.x, self.y)] = self.monster_id
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE
        
    def is_valid_move(self, x, y, col_map):
        if col_map[y][x] == 0:
            return True
        else:
            return False

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 1:
            self.dead = True

    def get_hp(self, num_of_dice):
        """Get initial hitpoints, level * D8"""
        total = 0
        for i in range(num_of_dice):
            total += random.randrange(1,9)
        return total

    def in_panic(self):
        roll = (random.randrange(6) + 1) + (random.randrange(6) + 1)
        if roll > self.morale:
            return True
        else:
            return False

    def get_weapon_damage(self):
        if self.current_weapon is not None:
            return self.current_weapon.max_damage
        else:
            return 0

    def do_turn(self, player, player_map, collision_map, monster_map):
        self.ai.update(self, player, player_map, collision_map, monster_map)
        print(self.name + " " + str(self.monster_id) + " has moved")