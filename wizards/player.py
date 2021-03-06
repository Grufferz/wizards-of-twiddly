import pygame, os, random
import wizards.constants, wizards.player_stats, wizards.bags


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.orig_hp = random.randrange(10,20) + 10
        self.hp = self.orig_hp
        self.max_magic = 50
        self.magic = self.max_magic
        self.magic_restore = 2
        self.spell_list = []
        fb = wizards.spells.Spell("Fireball", 1, 0, True, None, 6)
        self.spell_list.append(fb)
        charm = wizards.spells.Spell("Charm", 2, 0, True, None, 3)
        self.spell_list.append(charm)
        stone = wizards.spells.Spell("Stoneskin", 3, 0, True, None, None)
        self.spell_list.append(stone)
        self.cur_spell = self.spell_list[0]
        self.spell_index = 0
        self.active_spells = []

        self.inventory = []
        self.current_item = None
        self.item_index = 0

        self.gold = 0
        self.hand_weapon = None
        self.current_armour = None
        self.initial_ac = 7
        self.ac = self.initial_ac
        self.ac_missiles = self.ac
        self.ac_missiles_init = self.ac_missiles

        self.hit_chance = wizards.bags.NumberBag(1, 20, 2)

        self.dead = False
        self.dead_countdown = 120
        self.sight = 30
        self.xp = 0
        self.level = 1
        self.game_level = 1

        # game stats
        self.stats = {}
        self.total_monsters_killed = {}
        self.mons_killed_melee = 0
        self.mons_killed_magic = 0
        self.total_monsters_on_level = 0
        self.best_steps_for_level = 0
        self.steps_taken = 0


        self.carry_weight = 0

        self.image_name = "player_blank2.png"
        self.image = pygame.image.load(os.path.join("data", self.image_name)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def init_image(self):
        self.image = pygame.image.load(os.path.join("data", self.image_name)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def prepare_to_store(self):
        self.image = None
        self.rect = None

    def update_player(self, direction, col_map):

        new_x = self.x
        new_y = self.y
        if direction == 0:
            new_y = self.y - 1
        elif direction == 1:
            new_x = self.x + 1
        elif direction == 2:
            new_y = self.y + 1
        elif direction == 3:
            new_x = self.x - 1
        elif direction == 4:
            new_x = self.x + 1
            new_y = self.y -1
        elif direction == 5:
            new_x = self.x + 1
            new_y = self.y + 1
        elif direction == 6:
            new_x = self.x - 1
            new_y = self.y + 1
        elif direction == 7:
            new_x = self.x - 1
            new_y = self.y - 1

        if self.is_valid_move(new_x, new_y, col_map):
            #col_map[self.y][self.x] = 0
            #col_map[new_y][new_x] = 1
            self.x = new_x
            self.y = new_y

        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def is_valid_move(self, x, y, col_map):
        if x < 0 or y < 0 or x >= wizards.constants.WIDTH or y >= wizards.constants.HEIGHT:
            return False
        if col_map[y][x] == 0:
            return True
        else:
            return False

    def get_pos_tuple(self):
        return (self.x, self.y)

    def can_cast_spell(self, cost):
        return self.magic >= cost

    def deplete_magic(self, cost):
        self.magic -= cost
        if self.magic < 0:
            self.magic = 0

    def get_magic_percent(self):
        ret_p = int((self.magic / self.max_magic) * 100)
        return ret_p

    def restore_magic(self, m):
        self.magic += m
        if self.magic > self.max_magic:
            self.magic = self.max_magic

    def get_hp_percent(self):
        ret_p = int((self.hp / self.orig_hp) * 100)
        return ret_p

    def restore_health(self, amount):
        self.hp += amount
        if self.hp > self.orig_hp:
            self.hp = self.orig_hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 1:
            self.dead = True

    def add_inventory_item(self, item):
        self.inventory.append(item)
        self.carry_weight += item.weight

    def set_current_weapon(self, weapon):
        if weapon.equipment:
            self.hand_weapon = weapon

    def get_weapon_damage(self):
        if self.hand_weapon is not None:
            d = self.hand_weapon.max_damage + self.hand_weapon.adjuster
            return d
        else:
            return 0

    def add_xp(self, amount):
        self.xp += amount

    def add_item_to_inventory(self, item):
        if item.type == wizards.constants.GOLD:
            #for itm in self.inventory:
             #   if itm.type == wizards.constants.GOLD:
              #      itm.value += item.value
            self.gold += item.value
        else:
            self.carry_weight += item.weight
            self.inventory.append(item)
        self.get_gold_amount()

    def get_gold_amount(self):
        return self.gold

    def cycle_cur_item_up(self):
        if len(self.inventory) > 0:
            next_index = self.item_index + 1
            if next_index >= len(self.inventory):
                next_index = 0
            self.current_item = self.inventory[next_index]
            self.item_index = next_index

    def cycle_cur_item_down(self):
        if len(self.inventory) > 0:
            next_index = self.item_index - 1
            if next_index < 0:
                next_index = len(self.inventory)-1
            self.current_item = self.inventory[next_index]
            self.item_index = next_index

    def get_current_item(self):
        return self.inventory[self.item_index]

    def get_current_item_string(self):
        return self.inventory[self.item_index].get_description()

    def remove_current_item(self):
        self.inventory.remove(self.inventory[self.item_index])
        self.item_index = 0
        if len(self.inventory) > 0:
            self.current_item = self.inventory[self.item_index]
        else:
            self.current_item = None

    def use_current_item(self):
        msg = ""
        if len(self.inventory) > 0:
            if self.inventory[self.item_index].use:
                msg = self.inventory[self.item_index].use_object()
                if self.inventory[self.item_index].uses > 0:
                    self.remove_current_item()
                if self.inventory[self.item_index].weapon:
                    self.set_current_weapon(self.inventory[self.item_index])
        return msg

    def init_stats(self, tot, steps):
        self.mons_killed_magic = 0
        self.mons_killed_melee = 0
        self.total_monsters_on_level = tot
        self.best_steps_for_level = steps
        self.steps_taken = 0

    def set_stats_for_level(self, level):
        kp = self.get_monsters_kill_percent(level)
        speed = self.get_steps_percentage()
        if self.total_monsters_killed[level] > 0:
            magic = int((self.mons_killed_magic / self.total_monsters_killed[level]) * 100)
            melee = int((self.mons_killed_melee / self.total_monsters_killed[level]) * 100)
        else:
            magic = 0
            melee = 0

        self.stats[level] = wizards.player_stats.PlayerStats(speed, kp, magic, melee)

    def get_monsters_kill_percent(self, l):
        return int((self.total_monsters_killed[l] / self.total_monsters_on_level) * 100)

    def get_steps_percentage(self):
        return int((self.steps_taken / self.best_steps_for_level) * 100)
