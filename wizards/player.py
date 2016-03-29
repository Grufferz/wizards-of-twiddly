import pygame, os, random
import wizards.constants


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
        fb = wizards.spells.Spell("Fireball", 1, True, None, 6)
        self.spell_list.append(fb)
        charm = wizards.spells.Spell("Charm", 2, True, None, 3)
        self.spell_list.append(charm)
        self.cur_spell = self.spell_list[0]
        self.spell_index = 0
        self.inventory = []
        self.gold = 0
        self.hand_weapon = None
        self.current_armour = None
        self.ac = 9
        self.dead = False
        self.sight = 40
        self.xp = 0
        self.level = 1
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

    def updatePlayer(self,direction,col_map):

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

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 1:
            self.dead = True

    def add_inventory_item(self, item):
        self.inventory.append(item)

    def set_current_weapon(self, weapon):
        if weapon.equipment:
            self.hand_weapon = weapon

    def get_weapon_damage(self):
        if self.hand_weapon is not None:
            return self.hand_weapon.max_damage
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

