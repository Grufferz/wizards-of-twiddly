import pygame, os, wizards.constants
import constants

class WallSprite(pygame.sprite.Sprite):
   
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        #self.image = pygame.image.load("wall.png")
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.x = (x * wizards.constants.CHAR_SIZE)
        self.rect.y = (y * wizards.constants.CHAR_SIZE)