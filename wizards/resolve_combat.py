import random

class CombatResolver():

    def __init__(self):
        self.monster_attacks = [ [20,20,20,19,18,17,16,15,14,13,12,11,10],
                                 [20,20,19,18,17,16,15,14,13,12,11,10,9],
                                 [20,19,18,17,16,15,14,13,12,11,10,9,8],
                                 [19,18,17,16,15,14,13,12,11,10,9,8,7],
                                 [18,17,16,15,14,13,12,11,10,9,8,7,6],
                                 [17,16,15,14,13,12,11,10,9,8,7,6,5],
                                 [16,15,14,13,12,11,10,9,8,7,6,5,4]
                                 ]

        self.player_attack = [20,20,20,19,18,17,16,15,14,13,12,11,10]

        self.xp_table = [5,10,20,35,75,175,275]

    def resolve_player_hit(self, player, monster, dead_monsters, cur_level):
        # TODO Create combat system
        hd = monster.armour_rating + 3
        if hd < 0:
            hd = 0
        if hd > 12:
            hd = 12
        roll = random.randrange(20) + 1 + player.hand_weapon.adjuster
        print(str(roll) + " >> " + str(self.player_attack[hd]))
        if roll >= self.player_attack[hd]:
            dmg = player.get_weapon_damage()
            monster.take_damage(dmg)
        else:
            dmg = 0
        # if monster is dead add XP
        if monster.dead:
            i = monster.level
            if i > 6:
                i = 6
            xp = self.xp_table[i]
            xp *= monster.xp_mod
            xp = int(xp)
            player.add_xp(xp)
            dead_monsters += 1
            player.total_monsters_killed[cur_level] += 1
        return dmg

    def get_xp_for_monster(self, level):
        if level > 6:
            level = 6
        return self.xp_table[level]

