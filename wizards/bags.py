import random


class TFBag():

    def __init__(self, low, high, to_hit, size):
        self._bag = []
        self._range = 1 + high - low

        self._hit_chance = 1 + high - to_hit
        self._misses = 1 + high - low - self._hit_chance
        self._size = size
        self.init_bag()

    def init_bag(self):
        for x in range(self._size):
            for i in range(self._misses):
                self._bag.append(False)
            for i in range(self._hit_chance):
                self._bag.append(True)

        random.shuffle(self._bag)

    def draw(self):
        if len(self._bag) < 1:
            self.init_bag()

        num = self._bag.pop(0)
        return num


class NumberBag():

    def __init__(self, low, high, repeats):
        self._bag = []
        self._range = 1 + high - low
        self._size = repeats
        self._low = low
        self._high = high

        self.init_bag()

    def init_bag(self):
        val = self._low
        counter = self._low
        max_num = self._high * self._size
        while counter <= max_num:
            self._bag.append(val)
            counter += 1
            val += 1
            if val > self._high:
                val = self._low
        random.shuffle(self._bag)

    def draw(self):
        if len(self._bag) < 1:
            self.init_bag()

        num = self._bag.pop(0)
        return num

