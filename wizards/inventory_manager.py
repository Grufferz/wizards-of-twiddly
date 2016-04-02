import random
import wizards.constants, wizards.inventory_object, wizards.w_rand

class InventoryManager():

    def __init__(self):
        self._itemcount = 1

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

    def add_sword(self, x, y, t_ma, adj):
        name = "Sword"
        value = (random.randrange(6)+ 1) * 2
        sword = wizards.inventory_object.Sword(self._itemcount, x, y, name, wizards.constants.WEAPON, True,
                                               value, adj)
        self._itemcount += 1
        return sword

    def add_sword_to_character(self, adjuster=None, value=None):
        name = "Sword"
        if adjuster is None:
            adjuster = 0
        if value is None:
            value = random.randrange(2,7)
        sword = wizards.inventory_object.Sword(self._itemcount, 0, 0, name, wizards.constants.WEAPON, True,
                                               value, adjuster)
        self._itemcount += 1
        return sword

    def add_healing_potion(self):
        potion = wizards.inventory_object.Potion(self._itemcount, 0, 0, 'Healing Potion',
                                                 wizards.constants.POTION, True, 1, 1)
        self._itemcount += 1
        return potion

    def add_potion_with_location(self, x, y, t_map):
        potion = wizards.inventory_object.Potion(self._itemcount, x, y, 'Healing Potion', wizards.constants.POTION,
                                                 True, 1, 1)
        potion.init_image()

        t_map[y][x] = self._itemcount
        self._itemcount += 1
        return potion

    def add_random_item(self, x, y, t_map):

        ran = wizards.w_rand.WeightedRandomGuesser()
        # gold
        ran.add_bucket(1, 10)
        # sword
        ran.add_bucket(2, 1)
        #potion
        ran.add_bucket(3, 3)

        ran.init_buckets()
        treasure = None
        result = ran.get_random()
        if result  < 2:
            value = random.randrange(20) + 1
            treasure = wizards.inventory_object.Gold(self._itemcount, x, y, 'Gold', wizards.constants.GOLD, False, value)
        elif result == 2:
            # TODO create random sword selecter
            value = random.randrange(3) + 1
            ad_ran = random.randrange(10) + 1
            if ad_ran > 8:
                adj = 1
            else:
                adj = 0
            treasure = wizards.inventory_object.Sword(self._itemcount, x, y, 'Sword', wizards.constants.WEAPON, True, value, adj)
        elif result == 3:
            # TODO create random potion selecter
            treasure = wizards.inventory_object.Potion(self._itemcount, x, y, 'Healing Potion', wizards.constants.POTION, True, 1, 1)

        t_map[y][x] = self._itemcount
        treasure.init_image()
        self._itemcount += 1
        return treasure