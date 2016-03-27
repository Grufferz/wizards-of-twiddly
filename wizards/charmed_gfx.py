import pygame
import constants

class Charmed(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()    
        self.image = pygame.image.load("charmed.png").convert_alpha()
        self.image.convert() 
        self.rect = self.image.get_rect()
        self.rect.x = x * 16
        self.rect.y = y * 16
        #self.rect.centerx = x
        #self.rect.centery = y
        self.x = x
        self.y = y