import pygame, os
import wizards.constants

class InventoryObject(pygame.sprite.Sprite):

    def __init__(self, item_id, x, y, itemname, equipment=False, owner=None, value=None):
        super().__init__()
        self.item_id = item_id
        self.x = x
        self.y = y
        self.itemname = itemname
        self.value = value
        self.equipment = equipment
        self.owner = owner

    def get_id(self):
        return self.item_id

    def __str__(self):
        return self.itemname


class Gold(InventoryObject):

    def __init__(self, item_id, x, y, itemname, equipment, owner, value):
        super().__init__(item_id, x, y, itemname, equipment, owner, value)
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE


class Sword(InventoryObject):

    def __init__(self, item_id, x, y, itemname, equipment, owner, value, adjuster):
        super().__init__(item_id, x, y, itemname, equipment, owner, value)
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.adjuster = adjuster
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE
        self.max_damage = 6
        # TODO Work out weapon damages

