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
        #t_map[y][x] = self._itemcount
        t_map[(y,x)] = self._itemcount
        self._itemcount += 1
        return gold

    def add_short_bow_to_monster(self, x, y):

        name = "Short Bow"
        value = 10
        bow = wizards.inventory_object.ShortBow(self._itemcount, x, y, name, wizards.constants.WEAPON, True, value, 0)
        self._itemcount += 1
        return bow

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

        #t_map[y][x] = self._itemcount
        t_map[(y, x)] = self._itemcount
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
                value *= 2
            else:
                adj = 0
            treasure = wizards.inventory_object.Sword(self._itemcount, x, y, 'Sword', wizards.constants.WEAPON, True, value, adj)
        elif result == 3:
            # TODO create random potion selecter
            treasure = wizards.inventory_object.Potion(self._itemcount, x, y, 'Healing Potion', wizards.constants.POTION, True, 1, 1)

        #t_map[y][x] = self._itemcount
        t_map[(y, x)] = self._itemcount
        treasure.init_image()
        self._itemcount += 1
        return treasure

    def add_weighted_random_treasure_drop(self, monster, t_map):
        ran = wizards.w_rand.WeightedRandomGuesser()
        return_treasure = None
        if monster.treasure_drop is not None:
            nothing = monster.treasure_drop.nothing_chance
            if nothing > 0:
                ran.add_bucket(0, monster.treasure_drop.nothing_chance)
            if monster.treasure_drop.gold_chance > 0:
                ran.add_bucket(1, monster.treasure_drop.gold_chance)
            if monster.treasure_drop.potion_chance > 0:
                ran.add_bucket(2, monster.treasure_drop.potion_chance)
            if monster.treasure_drop.scroll_chance > 0:
                ran.add_bucket(3, monster.treasure_drop.scroll_chance)
            if monster.treasure_drop.rand_magic_chance > 0:
                ran.add_bucket(4, monster.treasure_drop.rand_magic_chance)

            ran.init_buckets()
            result = ran.get_random()
        else:
            result = 0
            print("No Drop")

        if result == 0:
            print("Nothing Drop")
        if result == 1:
            value = random.randrange(monster.treasure_drop.gold_min, monster.treasure_drop.gold_max) + 1
            return_treasure = self.add_gold(monster.x, monster.y, t_map, value)
        if result == 2:
            print("POTION")
            # TODO Add random potion drops
        if result == 3:
            print("SCROLL")
            # TODO Add random scroll drops
        if result > 3:
            print("RANDOM MAGIC TREASURE")
            # TODO Add random magic drops

        return return_treasure
