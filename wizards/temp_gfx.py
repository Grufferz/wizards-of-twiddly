import pygame, os, wizards.constants

class TempGraphic(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("data", "yellow.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.CHAR_SIZE
        self.rect.y = y * wizards.constants.CHAR_SIZE