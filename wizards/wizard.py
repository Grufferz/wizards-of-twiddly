import pygame, random, os
from wizards.base_monster import BaseMonster
import wizards.constants

class Wizard(BaseMonster):
    def __init__(self,x,y,name):
        super().__init__(x,y,name)
        self.image = pygame.image.load(os.path.join("data", "wizard1.png")).convert()
        #self.image = pygame.image.load("wizard1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE
        
        self.orig_hp = random.randrange(20,30) + 18
        self.hp = self.orig_hp   
        self.magic_resistance = 8 + random.randrange(1,6)
        self.charmed = False
        self.charmed_by = None
        self.charm_gfx = None