import pygame, wizards.constants, os

class DeadGraphic(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("data", "dead_txt.png"))
        #self.image.set_colorkey((0,0,0))
        self.image.convert() 
        self.img_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.x = (x * wizards.constants.CHAR_SIZE) - 10
        self.y = (y * wizards.constants.CHAR_SIZE) - 10
        self.rect.x = x * wizards.constants.CHAR_SIZE - 10
        self.rect.y = y * wizards.constants.CHAR_SIZE - 10
        self.lifespan = 74
        self.scale_x = 34
        self.scale_y = 26
        self.zoomfactor = 1