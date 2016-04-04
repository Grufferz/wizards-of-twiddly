import pygame, random, os
from wizards.base_monster import BaseMonster
import wizards.constants, wizards.treasure_drop


class Wizard(BaseMonster):
    def __init__(self, mid, x, y, name, level, m_type):
        super().__init__(mid, x, y, name, level, m_type)
        self.monster_id = mid
        self.image = pygame.image.load(os.path.join("data", "wizard1.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE

        self.morale = 10
        self.armour_rating = 4
        self.xp_mod = 1.4
        self.save_magic = 15
        self.charmable = True
        self.charmed = False
        self.charmed_by = None
        self.charm_gfx = None

        self.native_depth = 15
        self.t = wizards.constants.WIZARD

        rand_chance = 10 * self.level
        rand_chance = min(30, rand_chance)
        self.treasure_drop = wizards.treasure_drop.TreasureDrop(25, 1, 8, 0, 25, rand_chance)

    def set_weight(self, lev):
        w = 15 - abs(self.native_depth - lev)
        w = max(w, 0)
        w = min(w, 10)

        self.weight = w

    def init_image(self):
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE
