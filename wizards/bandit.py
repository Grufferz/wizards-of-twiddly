import pygame, os, random
from wizards.base_monster import BaseMonster
import wizards.constants

class Bandit(BaseMonster):
    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)
        self.monster_id = mid
        self.image = pygame.image.load(os.path.join("data", "bandit.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE

        self.morale = 8
        self.armour_rating = 6
        self.xp_mod = 1
        self.save_magic = 15
        