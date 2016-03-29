import pygame, os
from wizards.constants import *
import wizards.loading_screen, wizards.constants

class TitleScreen(object):
    
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
        
    def render(self, screen):
        screen.fill(BLACK)
        text1 = self.font.render('Wizards!', True, WHITE)
        #TODO Decide between new game or loading old one
        text2 = self.sfont.render('Press SPACE', True, WHITE)
        screen.blit(text1, (400,200))
        screen.blit(text2, (400,300))
    
    def update(self):
        pass
    
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.manager.go_to(wizards.loading_screen.LoadingScreen(1))
