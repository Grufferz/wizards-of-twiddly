import pygame, wizards.constants, random, os

class MagicSpell(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()  
        self.x = x * wizards.constants.CHAR_SIZE
        self.y = y * wizards.constants.CHAR_SIZE
        displace_x = random.randrange(40) - 20
        displace_y = random.randrange(40) - 20
        self.x += displace_x
        self.y += displace_y
        self.lifespan = random.randrange(80) + 20
        self.image = pygame.image.load(os.path.join("data", "mag.png"))
        self.image.convert_alpha()
        self.image.convert() 
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
        
    
    def update(self):
        self.lifespan -= 1
        if self.lifespan < 1:
            self.kill()
        mx = random.randrange(3) - 1
        my = random.randrange(3) - 1
        self.rect.x += mx
        self.rect.y += my         