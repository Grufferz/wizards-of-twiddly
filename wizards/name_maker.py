import random, os

class NameMaker():

    def __init__(self):
        pass

    def get_firstname(self):
        f = open( os.path.join('wizards', 'firstnames.txt'), 'r')
        lines = f.readlines()
        f.close()
        name = random.choice(lines)
        name = name.strip('\n')
        return name

    def get_second(self):
        f = open(os.path.join('wizards', 'the.txt'), 'r')
        lines = f.readlines()
        f.close()
        name = random.choice(lines)
        name = name.strip('\n')
        return name

    def generate_name(self):
        first = self.get_firstname()
        second = self.get_second()
        ret_name = first + " " + second
        return ret_name


