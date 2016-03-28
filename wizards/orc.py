import pygame, random, os
from wizards.base_monster import BaseMonster
import wizards.constants

class Orc(BaseMonster):
    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)
        self.monster_id = mid
        self.image = pygame.image.load(os.path.join("data", "orc.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE

        self.armour_rating = 6
        self.morale = 8
        self.xp_mod = 1
        self.save_magic = 16
        self.charmable = True
        self.charmed = False
        self.charmed_by = None
        self.charm_gfx = None

        
