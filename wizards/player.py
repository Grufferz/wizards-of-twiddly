import pygame, os, random
import wizards.constants

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("data", "player_blank2.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE
        self.x = x
        self.y = y
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
        self.hand_weapon = None
        self.dead = False
        self.sight = 40
        self.xp = 0
        self.level = 1
        
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
 
