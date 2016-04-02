import random


class Bucket():

    def __init__(self, guess_type, width ):
        self.width = width
        self.edge = 0
        self.guess_type = guess_type

    def __repr__(self):
        return '{}: {}'.format(self.guess_type, self.edge)

    def __cmp__(self, other):
        return cmp(self.edge, other.edge)


class WeightedRandomGuesser():

    def __init__(self):
        self._max_index = 0
        self.guesses = []

    def add_bucket(self, g_type, width):

        cur_bucket = Bucket(g_type, width)
        self.guesses.append(cur_bucket)

    def init_buckets(self):
        self.guesses.sort(key=lambda x: x.width)
        for x in range(len(self.guesses)):

            this_size = self.guesses[x].width

            if x == 0:
                self.guesses[x].edge = this_size
            else:
                self.guesses[x].edge = self.guesses[x-1].edge + this_size

        #self.guesses.sort(key=lambda x: x.edge)

    def get_random(self):
        self.guesses.sort(key=lambda x: x.edge)
        num_buckets= len(self.guesses)
        first = 0
        last = len(self.guesses) - 1
        found = False
        max_roll = self.guesses[num_buckets-1].edge
        target = random.randrange(max_roll)
        while first <= last and not found:
            midpoint = (first + last)//2

            if self.in_bucket(midpoint, target):
                return self.guesses[midpoint].guess_type
            if target < self.guesses[midpoint].edge:
                last = midpoint - 1
            else:
                first = midpoint + 1
        return 0

    def in_bucket(self, i, target):
        if i == 0 and target <= self.guesses[i].edge:
            return True
        if target <= self.guesses[i].edge and target > self.guesses[i-1].edge:
            return True
        else:
            return False



#b1 = WeightedRandomGuesser()
#b1.add_bucket(1,10)
#b1.add_bucket(3,30)
#b1.add_bucket(2,50)
#b1.add_bucket(4,100)
#b1.init_buckets()
#for i in range(50):
#    t = b1.bin_search_2()
#    print(str(t))



