import pygame, random
import wizards.constants

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

        # TODO Monster AI

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
        """GEt initial hitpoints, level * D8"""
        total = 0
        for i in range(num_of_dice):
            total += (random.randrange(0,8)+1)
        return total