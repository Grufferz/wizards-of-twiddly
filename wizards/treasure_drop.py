

class TreasureDrop():

    def __init__(self, gold_chance, gold_min, gold_max, potion_chance, scroll_chance, rand_magic_chance):
        self.gold_chance = gold_chance
        self.gold_min = gold_min
        self.gold_max = gold_max
        self.potion_chance = potion_chance
        self.scroll_chance = scroll_chance
        self.rand_magic_chance = rand_magic_chance
        self.nothing_chance = 100 - self.gold_chance - self.potion_chance - self.scroll_chance - self.rand_magic_chance
        self.nothing_chance = max(0, self.nothing_chance)