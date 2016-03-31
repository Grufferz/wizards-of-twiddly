import pygame, os
import wizards.constants

class Charmed(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("data", "charmed.png"))
        self.image.convert_alpha()
        self.image.convert() 
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE
        #self.rect.centerx = x
        #self.rect.centery = y
        self.x = x
        self.y = y