import pygame
from wizards.constants import *
import wizards.loading_screen, wizards.constants

class ExitScreen(object):

    def __init__(self, player, level_num):
        super(ExitScreen, self).__init__()
        self.player = player
        self.level_num = level_num

        self.font = pygame.font.SysFont('Arial', 40)
        self.sfont = pygame.font.SysFont('Arial', 24)

    def render(self, screen):
        screen.fill(BLACK)
        text1 = self.font.render(self.player.name, True, WHITE)
        text2 = self.sfont.render('Press SPACE', True, WHITE)
        text3 = self.sfont.render('Exiting Level ' + str(self.level_num), True, WHITE)
        text4 = self.sfont.render('Experience Gained: ' + str(self.player.xp), True, WHITE)
        text5 = self.sfont.render('Gold Gathered: ' + str(self.player.get_gold_amount()), True, WHITE)
        text6 = self.sfont.render('Saving Game', True, WHITE)
        screen.blit(text1, (400, 100))
        screen.blit(text3, (400, 200))
        screen.blit(text4, (400, 300))
        screen.blit(text5, (400, 400))
        screen.blit(text6, (400, 500))
        screen.blit(text2, (400, 600))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.manager.go_to(wizards.loading_screen.LoadingScreen(1))
