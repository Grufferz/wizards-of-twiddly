

class WRObject():

    def __init__(self, t, name, prob, boss, special):
        self.type = int(t)
        self.name = name
        self.probability = int(prob)
        if boss == "TRUE":
            self.boss = True
        else:
            self.boss = False
        if special == "TRUE":
            self.special = True
        else:
            self.special = False
        self.weight = 0

    def set_weight(self, level):
        if not self.boss:
            w = 15 - abs(self.probability - level)
            w = max(w, 0)
            w = min(w, 10)
            self.weight = w
        else:
            w = level - 20
            w = max(w, 0)
            self.weight = w
