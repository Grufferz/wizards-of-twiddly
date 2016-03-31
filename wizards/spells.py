import random


class Spell(object):
    
    def __init__(self, name, t, uses, area=False, rge=None, r=None):
        self.name = name
        self.spell_type = t
        self.range = rge
        self.radius = r
        self.duration = -1
        self.area_based = area
        self.damage = None
        self.expired = False
        self.uses = uses

        # fireball
        if self.spell_type == 1:
            self.damage = 6
            self.magic_cost = 25
        # charm
        if self.spell_type == 2:
            self.magic_cost = 50
        #stoneskin
        if self.spell_type == 3:
            self.magic_cost = 30
            self.duration = 4

    def set_duration(self, d):
        self.duration = d

    def get_charm_duration(self):
        total = 0
        for i in range(4):
            roll = random.randrange(4) + 1
            total += roll
        return total

    def test_charm(self, resist):
        roll = random.randrange(20)+1
        if roll >= 17 or roll > resist:
            return True
        else:
            return False

    def update_spell(self):
        if self.duration > -1:
            self.duration -= 1
            if self.duration == 0:
                self.expired = True
