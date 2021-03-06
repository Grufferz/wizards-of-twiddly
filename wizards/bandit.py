import pygame, os, random
from wizards.base_monster import BaseMonster
import wizards.constants, wizards.treasure_drop

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

        self.native_depth = 5
        self.t = wizards.constants.BANDIT

        self.orig_hp = self.get_hp(level) * 8
        self.hp = self.orig_hp

        self.treasure_drop = wizards.treasure_drop.TreasureDrop(5, 1, 100, 0, 0, 2)

    def set_weight(self, lev):
        w = 15 - abs(self.native_depth - lev)
        w = max(w, 0)
        w = min(w, 10)
        self.weight = w

    def init_image(self):
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE


class BanditArcher(Bandit):

    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)


class BanditLeader(Bandit):

    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)
        self.morale = 12

class BanditBezerker(Bandit):
    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)
        self.morale = 12
        self.never_surrender = True
        self.orig_hp = self.get_hp(level)  + self.level
        self.hp = self.orig_hp


