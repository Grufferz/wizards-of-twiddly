import random, wizards.constants, wizards.bandit, wizards.orc, wizards.skeleton, wizards.wizard
import wizards.w_rand

class MonsterGenerator():
    
    def __init__(self, level, mm, level_score):
        self.level = level
        self.monster_map = mm
        self.level_score = level_score
        self.monster_count = 0

    def return_monster_list(self, positions, im, mt, level):
        
        ret_list = []

        if mt == wizards.constants.WANDERING:
            m_type = "Wandering"
        else:
            m_type = "Lair"

        for p in positions:
            self.monster_count += 1
            roll = random.randrange(0, 5) + 1 + self.level
            level_roll = random.randrange(0, 1) + 1
            if self.level_score == 12:
                roll += 2
            x = p[0]
            y = p[1]
            if roll <= 3:
                ret_monster = wizards.orc.Orc(self.monster_count, x, y, "Orc", level_roll, m_type)
                sword = im.add_sword_to_character()
                sword.set_owner(ret_monster)
                ret_monster.current_weapon = sword
            elif roll > 3 and roll < 6:
                ret_monster = wizards.bandit.Bandit(self.monster_count, x, y, "Bandit", level_roll, m_type)
                sword = im.add_sword_to_character()
                ret_monster.current_weapon = sword
                sword.set_owner(ret_monster)
            elif roll == 6:
                ret_monster = wizards.skeleton.Skeleton(self.monster_count, x, y, "Skeleton", level_roll, m_type)
                sword = im.add_sword_to_character()
                ret_monster.current_weapon = sword
                sword.set_owner(ret_monster)
            elif roll > 6:
                ret_monster = wizards.wizard.Wizard(self.monster_count, x, y, "Wizard", level_roll, m_type)
                # TODO Add hand weapon for wizards
            self.monster_map[y][x] = self.monster_count
            ret_list.append(ret_monster)
        
        return ret_list
    
    def return_single_monster(self, x, y, mt):

        if mt == wizards.constants.WANDERING:
            m_type = "Wandering"
        else:
            m_type = "Lair"
        
        ret_monster = None
        self.monster_count += 1
        roll = random.randrange(0,5) + 1 + self.level
        
        if roll <= 2:
            ret_monster = wizards.orc.Orc(self.monster_count, x , y, "Orc",m_type)
        elif roll > 2 and roll < 6:
            ret_monster = wizards.bandit.Bandit(self.monster_count, x, y, "Bandit", m_type)
        elif roll == 6:
            ret_monster = wizards.skeleton.Skeleton(self.monster_count, x, y, "Skeleton", m_type)
        elif roll > 6:
            ret_monster = wizards.wizard.Wizard(self.monster_count, x, y, "Wizard", m_type)
        
        return ret_monster

    def get_number_of_monsters(self):
        return self.monster_count

    def get_initial_monsters(self, positions, im, mt, level):
        ret_list = []
        m_type = "Wandering"
        x = 0
        y = 0
        random_getter = wizards.w_rand.WeightedRandomGuesser()

        orc = wizards.orc.Orc(self.monster_count, x, y, "Orc", 1, m_type)
        orc.set_weight(level)
        bandit = wizards.bandit.Bandit(self.monster_count, x, y, "Bandit", 1, m_type)
        bandit.set_weight(level)
        skeleton = wizards.skeleton.Skeleton(self.monster_count, x, y, "Skeleton", 1, m_type)
        skeleton.set_weight(level)
        wizard = wizards.wizard.Wizard(self.monster_count, x, y, "Wizard", 1, m_type)
        wizard.set_weight(level)

        random_getter.add_bucket(wizards.constants.ORC, orc.weight)
        random_getter.add_bucket(wizards.constants.BANDIT, bandit.weight)
        random_getter.add_bucket(wizards.constants.SKELETON, skeleton.weight)
        random_getter.add_bucket(wizards.constants.WIZARD, wizard.weight)

        random_getter.init_buckets()

        for p in positions:
            self.monster_count += 1
            roll = random_getter.get_random()
            level_roll = random.randrange(0, 1) + 1
            if self.level_score == 12:
                roll += 2
            x = p[0]
            y = p[1]
            if roll == wizards.constants.ORC:
                ret_monster = wizards.orc.Orc(self.monster_count, x, y, "Orc", level_roll, m_type)
                sword = im.add_sword_to_character()
                sword.set_owner(ret_monster)
                ret_monster.current_weapon = sword
            elif roll == wizards.constants.BANDIT:
                ret_monster = wizards.bandit.Bandit(self.monster_count, x, y, "Bandit", level_roll, m_type)
                sword = im.add_sword_to_character()
                ret_monster.current_weapon = sword
                sword.set_owner(ret_monster)
            elif roll == wizards.constants.SKELETON:
                ret_monster = wizards.skeleton.Skeleton(self.monster_count, x, y, "Skeleton", level_roll, m_type)
                sword = im.add_sword_to_character()
                ret_monster.current_weapon = sword
                sword.set_owner(ret_monster)
            elif roll == wizards.constants.WIZARD:
                ret_monster = wizards.wizard.Wizard(self.monster_count, x, y, "Wizard", level_roll, m_type)
                # TODO Add hand weapon for wizards
            self.monster_map[y][x] = self.monster_count
            ret_list.append(ret_monster)

        return ret_list






