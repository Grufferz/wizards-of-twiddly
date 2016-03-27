import pygame, os, random
from wizards.base_monster import BaseMonster
import wizards.constants

class Skeleton(BaseMonster):
    def __init__(self,x,y,name):
        super().__init__(x,y,name)
        self.image = pygame.image.load(os.path.join("data", "skeleton.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE
        
        self.orig_hp = random.randrange(10,20) + 6
        self.hp = self.orig_hp   
        self.magic_resistance = 8 + random.randrange(1,6)
        self.charmed = False
        self.charmed_by = None
        self.charm_gfx = None
        