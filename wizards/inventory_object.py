import pygame, os, random
import wizards.constants


class InventoryObject(pygame.sprite.Sprite):

    def __init__(self, item_id, x, y, itemname, type, equipment=False, value=None):
        super().__init__()
        self.item_id = item_id
        self.x = x
        self.y = y
        self.itemname = itemname
        self.type = type
        self.value = value
        self.equipment = equipment
        self.wearable = False
        self.weapon = False
        self.owner = None
        self.magic = False
        self.use = False
        self.uses = 0
        #self.owner = owner

    def get_id(self):
        return self.item_id

    def set_owner(self, o):
        self.owner = o

    def get_description(self):
        return self.itemname

    def use_object(self):
        return "Nothing"

    def __str__(self):
        return self.itemname


class Gold(InventoryObject):

    def __init__(self, item_id, x, y, itemname, type, equipment, value):
        super().__init__(item_id, x, y, itemname, type, equipment, value)
        self.weight = 0

    def init_image(self):
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def prepare_to_store(self):
        self.image = None
        self.rect = None

    def get_description(self):
        if self.value == 1:
            rs = " Gold Piece"
        else:
            rs = " Gold Pieces"
        return str(self.value) + rs


class Potion(InventoryObject):

    def __init__(self, item_id, x, y, itemname, type, equipment, value, potion_type):
        super().__init__(item_id, x, y, itemname, type, equipment, value)
        self.potion_type = potion_type
        self.weight = 1
        self.use = True
        self.uses = 1
        self.strength = random.randrange(6) + 2
        if self.potion_type == 1:
            self.duration = 0
        else:
            self.duration = random.randrange(6) + 7

    def init_image(self):
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def prepare_to_store(self):
        self.image = None
        self.rect = None

    def use_object(self):
        if self.potion_type == 1:
            self.owner.restore_health(self.strength)
            ret = "Healed By " + str(self.strength)
            return ret


class ShortBow(InventoryObject):

    def __init__(self, item_id, x, y, itemname, type, equipment, value, adjuster=None):
        super().__init__(item_id, x, y, itemname, type, equipment, value)
        self.adjuster = adjuster
        if adjuster is not None:
            self.magic = True
        self.max_damage = 6
        self.weight = 3
        self.weapon = True
        self.use = True

        self.ranges = [10, 25, 35]


    def get_description(self):
        msg = self.itemname
        if self.adjuster > 0:
            msg += " +" + str(self.adjuster)
        elif self.adjuster < 0:
            msg += " -" + str(self.adjuster)
        return msg


class Sword(InventoryObject):

    def __init__(self, item_id, x, y, itemname, type, equipment, value, adjuster):
        super().__init__(item_id, x, y, itemname, type, equipment, value)
        self.adjuster = adjuster
        if adjuster > 0:
            self.magic = True
        self.max_damage = 6
        self.weight = 3
        self.weapon = True
        self.use = True
        # TODO Work out weapon damages

    def init_image(self):
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def prepare_to_store(self):
        self.image = None
        self.rect = None

    def get_description(self):
        msg = self.itemname
        if self.adjuster > 0:
            msg += " +" + str(self.adjuster)
        elif self.adjuster < 0:
            msg += " -" + str(self.adjuster)
        return msg