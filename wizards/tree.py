import pygame, os
import wizards.constants, random

class Tree(pygame.sprite.Sprite):
   
    def __init__(self,x,y):
        super().__init__()
        #r = random.randrange(100)
        #if r < 25:
            #self.image = pygame.image.load("tree_block.png").convert()  
        #elif r >= 25 and r < 40:
            #self.image = pygame.image.load("tree_block2.png").convert()
        #elif r >= 40 and r < 75:
            #self.image = pygame.image.load("tree_block3.png").convert()
        #elif r > 74:
            #self.image = pygame.image.load("tree_block4.png").convert() 
        #self.image = pygame.image.load("small_tree.png").convert()
        self.image = pygame.image.load(os.path.join("data", "small_tree.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x * wizards.constants.F_BLOCKS
        self.rect.y = y * wizards.constants.F_BLOCKS
        self.x = x
        self.y = y
        
    

