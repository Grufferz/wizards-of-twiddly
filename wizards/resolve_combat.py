import random

class CombatResolver():

    def __init__(self):
        pass

    def resolve_player_hit(self, player, monster):
        # TODO Create combat system
        dmg = player.get_weapon_damage()
        monster.take_damage(dmg)
        return dmg

