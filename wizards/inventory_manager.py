import random
import wizards.constants, wizards.inventory_object

class InventoryManager():

    def __init__(self):
        self._itemcount = 0

    def add_object(self):
        pass

    def add_gold(self, x, y, t_map, value=None, owner=None):
        name = "Gold"
        if value is None:
            value = random.randrange(5)+3
        if owner is not None:
            owner = owner
        gold = wizards.inventory_object.Gold(self._itemcount, x, y, name, wizards.constants.GOLD, False, owner, value)
        t_map[y][x] = self._itemcount
        self._itemcount += 1
        return gold

    def add_sword_to_character(self, owner, adjuster, value=None):
        name = "Sword"
        if value is None:
            value = random.randrange(2,7)
        sword = wizards.inventory_object.Sword(self._itemcount, owner.x, owner.y, name, wizards.constants.WEAPON, True, owner, value, adjuster)
        self._itemcount += 1
        return sword


