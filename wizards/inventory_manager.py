import random
import wizards.constants, wizards.inventory_object

class InventoryManager():

    def __init__(self):
        self._itemcount = 0

    def add_object(self):
        pass

    def add_gold(self, x, y, t_map, value=None):
        name = "Gold"
        if value is None:
            value = random.randrange(5)+3
        gold = wizards.inventory_object.Gold(self._itemcount, x, y, name, wizards.constants.GOLD, False, value)
        gold.init_image()
        t_map[y][x] = self._itemcount
        self._itemcount += 1
        return gold

    def add_sword_to_character(self, adjuster=None, value=None):
        name = "Sword"
        if adjuster is None:
            adjuster = 0
        if value is None:
            value = random.randrange(2,7)
        sword = wizards.inventory_object.Sword(self._itemcount, 0, 0, name, wizards.constants.WEAPON, True, value, adjuster)
        self._itemcount += 1
        return sword


