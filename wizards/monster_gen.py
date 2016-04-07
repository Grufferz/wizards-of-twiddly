import random, wizards.constants, wizards.bandit, wizards.orc, wizards.skeleton, wizards.wizard
import wizards.w_rand, wizards.w_rand_obj
import csv, os

class MonsterGenerator():
    
    def __init__(self, level, mm, level_score):
        self.level = level
        self.monster_map = mm
        self.level_score = level_score
        self.monster_count = 1

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
            #self.monster_map[y][x] = self.monster_count
            self.monster_map[(x,y)] = self.monster_count
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

    def get_initial_monsters(self, positions, im, mt, level, level_score):
        ret_list = []
        m_type = "Wandering"
        random_getter = wizards.w_rand.WeightedRandomGuesser()

        mons_list = self.load_monster_probs()
        # TODO Add special monsters for level_score = 12
        for i in mons_list:
            i.set_weight(level)
            if i.weight > 0:
                random_getter.add_bucket(i.type, i.weight)
        random_getter.init_buckets()
        for p in positions:
            m_id = random_getter.get_random()
            monster = None

            if m_id == 1:
                monster = self.create_bandit(self.monster_count, p[0], p[1], m_type, level, im)
            elif m_id == 2:
                monster = self.create_orc(self.monster_count, p[0], p[1], m_type, level, im)
            elif m_id == 3:
                monster = self.create_skeleton(self.monster_count, p[0], p[1], m_type, level, im)
            elif m_id == 4:
                monster = self.create_wizard(self.monster_count, p[0], p[1], m_type, level, im)

            ret_list.append(monster)

        return ret_list

    def create_bandit(self, id, x, y, m_type, level, im):

        bandit_prob = wizards.w_rand.WeightedRandomGuesser()
        bandit_prob.add_bucket(1, 7)
        bandit_prob.add_bucket(2, 4)
        bandit_prob.add_bucket(3, 1)
        bandit_prob.add_bucket(4, 1)
        bandit_prob.init_buckets()

        bandit_choice = bandit_prob.get_random()

        if bandit_choice == 1:

            bandit = wizards.bandit.Bandit(id, x, y, "Bandit", level, m_type)
            sword = im.add_sword_to_character()
            sword.set_owner(bandit)
            bandit.current_weapon = sword

        elif bandit_choice == 2:
            bandit = wizards.bandit.BanditArcher(id, x, y, "Bandit Archer", level, m_type)
            bow = im.add_short_bow_to_monster(0, 0)
            bow.set_owner(bandit)
            bandit.current_weapon = bow

        elif bandit_choice == 3:
            bandit = wizards.bandit.BanditLeader(id, x, y, "Bandit Leader", level + 2, m_type)
            sword = im.add_sword_to_character()
            sword.set_owner(bandit)
            bandit.current_weapon = sword

        elif bandit_choice == 4:
            bandit = wizards.bandit.BanditBezerker(id, x, y, "Bandit Bezerker", level, m_type)
            sword = im.add_sword_to_character()
            sword.set_owner(bandit)
            bandit.current_weapon = sword

        self.monster_count += 1
        return bandit

    def create_orc(self, id, x, y, m_type, level, im):
        mons = wizards.orc.Orc(id, x, y, "Orc", level, m_type)
        sword = im.add_sword_to_character()
        sword.set_owner(mons)
        mons.current_weapon = sword
        self.monster_count += 1
        return mons

    def create_skeleton(self, id, x, y, m_type, level, im):
        mons = wizards.skeleton.Skeleton(id, x, y, "Skeleton", level, m_type)
        sword = im.add_sword_to_character()
        sword.set_owner(mons)
        mons.current_weapon = sword
        self.monster_count += 1
        return mons

    def create_wizard(self, id, x, y, m_type, level, im):
        mons = wizards.wizard.Wizard(id, x, y, "Wizard", level, m_type)
        # TODO Add hand weapon for wizards
        #sword = im.add_sword_to_character()
        #sword.set_owner(mons)
        #mons.current_weapon = sword
        self.monster_count += 1
        return mons

    def load_monster_probs(self):
        ret_list = []
        ifile = open(os.path.join("wizards", "monsters_prob.csv"))
        reader = csv.reader(ifile)
        row_num = 0
        for row in reader:
            if row_num > 0:
                o = wizards.w_rand_obj.WRObject(row[1], row[0], row[2], row[3], row[4])
                ret_list.append(o)
            row_num += 1
        ifile.close()
        return ret_list



