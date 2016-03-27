import pygame
import constants, random

class BaseMonster(pygame.sprite.Sprite):
    def __init__(self,x,y, name):
        super().__init__()    
        self.x = x
        self.y = y        
        self.name = name
        self.orig_hp = 6
        self.hp = self.orig_hp  
        self.dead = False
        
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
            
        self.rect.x = self.x * constants.CHAR_SIZE
        self.rect.y = self.y * constants.CHAR_SIZE         
        
    def is_valid_move(self, x, y, col_map):
        if col_map[y][x] == 0:
            return True
        else:
            return False
        
    
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 1:
            self.dead = True