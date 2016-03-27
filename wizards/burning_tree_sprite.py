import pygame, os
import wizards.constants, random

class BurningTreeSprite(pygame.sprite.Sprite):
   
    def __init__(self,x,y, res, intensity):
        super().__init__()
        r = random.randrange(100)
        if r < 25:
            self.image = pygame.image.load(os.path.join("data", "fire2.png"))
        elif r >= 25:
            self.image = pygame.image.load(os.path.join("data", "fire1.png"))
        self.rect = self.image.get_rect()
        self.rect.x = (x * wizards.constants.F_BLOCKS)
        self.rect.y = (y * wizards.constants.F_BLOCKS)
        self.resistance = res
        self.intensity = intensity
        self.x = x
        self.y = y
        self.removed = False
        self.int_reduction = random.uniform(0.01, 0.02)

    def update(self):
        self.resistance -= self.intensity
        if self.intensity > 0:
            self.intensity -= self.int_reduction
        #else:
            #self.kill()
        if self.resistance < 1:
            self.kill()
            
