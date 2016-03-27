import random, wizards.constants, wizards.bandit,wizards.orc, wizards.skeleton, wizards.wizard


class MonsterGenerator():
    
    def __init__(self, level,level_score):
        self.level = level
        self.level_score = level_score
        
        
    def return_monster_list(self, positions):
        
        ret_list = []
        
        for p in positions:
            roll = random.randrange(0,5) + 1 + self.level
            if self.level_score == 12:
                roll += 2
            x = p[0]
            y = p[1]
            if roll <= 3:
                ret_monster = wizards.orc.Orc(x,y,"Orc")
            elif roll > 3 and roll < 6:
                ret_monster = wizards.bandit.Bandit(x,y,"Bandit")
            elif roll == 6:
                ret_monster = wizards.skeleton.Skeleton(x,y,"Skeleton")
            elif roll > 6:
                ret_monster = wizards.wizard.Wizard(x,y,"Wizard")
            
            ret_list.append(ret_monster)
        
        return ret_list
            
            
    
    def return_single_monster(self, x, y):
        
        ret_monster = None
        
        roll = random.randrange(0,5) + 1 + self.level
        
        if roll <= 2:
            ret_monster = wizards.orc.Orc(x,y,"Orc")
        elif roll > 2 and roll < 6:
            ret_monster = wizards.bandit.Bandit(x,y,"Bandit")
        elif roll == 6:
            ret_monster = wizards.skeleton.Skeleton(x,y,"Skeleton")
        elif roll > 6:
            ret_monster = wizards.wizard.Wizard(x,y,"Wizard")
        
        return ret_monster
    