import pygame, os, random
from wizards.base_monster import BaseMonster
import wizards.constants

class Skeleton(BaseMonster):
    def __init__(self,mid,x,y,name, level, m_type):
        super().__init__(mid,x,y,name, level, m_type)
        self.monster_id = mid
        self.image = pygame.image.load(os.path.join("data", "skeleton.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE

        self.armour_rating = 7
        self.morale = 12
        self.xp_mod = 1
        self.save_magic = 16
        self.charmable = False
        self.charmed = False
        self.charmed_by = None
        self.charm_gfx = None
        self.undead = True

        self.native_depth = 10
        self.t = wizards.constants.SKELETON

    def set_weight(self, lev):
        w = 15 - abs(self.native_depth - lev)
        w = max(w, 0)
        w = min(w, 10)

        self.weight = w

    def init_image(self):
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE