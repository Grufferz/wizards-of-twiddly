import pygame, os
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
        #self.owner = owner

    def get_id(self):
        return self.item_id

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


class Sword(InventoryObject):

    def __init__(self, item_id, x, y, itemname, type, equipment, value, adjuster):
        super().__init__(item_id, x, y, itemname, type, equipment, value)
        self.adjuster = adjuster
        self.max_damage = 6
        self.weight = 3
        # TODO Work out weapon damages

    def init_image(self):
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * wizards.constants.CHAR_SIZE
        self.rect.y = self.y * wizards.constants.CHAR_SIZE

    def prepare_to_store(self):
        self.image = None
        self.rect = None

