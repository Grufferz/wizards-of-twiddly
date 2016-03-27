

class Spell(object):
    
    def __init__(self, name, t, area=False, rge=None, r=None):
        self.name = name
        self.spell_type = t
        self.rge = rge
        self.radius = r
        self.area_based = area
        self.damage = None
        if self.spell_type == 1:
            self.damage = 6
            self.magic_cost = 25
        if self.spell_type == 2:
            self.magic_cost = 50