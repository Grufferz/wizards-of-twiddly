import pygame, os
from wizards.constants import *
import wizards.loading_screen, wizards.constants

# free font from: http://www.1001freefonts.com/imperator.font

class TitleScreen(object):
    
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.fontname = 'Imperator.ttf'
        #self.font = pygame.font.SysFont('Arial', 56)
        #self.sfont = pygame.font.SysFont('Arial', 32)

        self.font = pygame.font.Font(os.path.join('data', self.fontname), 60)
        self.sfont = pygame.font.Font(os.path.join('data', self.fontname), 36)


        self.continue_game = False

    def render(self, screen):
        screen.fill(BLACK)
        text1 = self.font.render('Wizards Of Twiddly!', True, WHITE)
        screen.blit(text1, (400, 200))
        #TODO Decide between new game or loading old one
        self.player = None
        if os.path.isfile(wizards.constants.PL_FILE):
            self.player = wizards.utils.load_zip(wizards.constants.PL_FILE)
            text3 = self.sfont.render('Continue With ' + self.player.name + " at Level " + str(self.player.game_level), True, WHITE)
            screen.blit(text3, (300, 300))
            self.continue_game = True
        text2 = self.sfont.render('Press Any Key', True, WHITE)

        screen.blit(text2, (300,400))
    
    def update(self):
        pass
    
    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if self.continue_game:
                    self.manager.go_to(wizards.loading_screen.LoadingScreen(self.player.game_level))
                else:
                    self.manager.go_to(wizards.loading_screen.LoadingScreen(1))
