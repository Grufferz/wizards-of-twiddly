

class WRObject():

    def __init__(self, t, name, prob, boss, special):
        self.type = int(t)
        self.name = name
        self.probability = int(prob)
        self.boss = boss
        self.special = special
        self.weight = 0

    def set_weight(self, level):
        w = 15 - abs(self.probability - level)
        w = max(w, 0)
        w = min(w, 10)
        self.weight = w