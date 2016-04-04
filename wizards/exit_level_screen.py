import pygame, os
from wizards.constants import *
import wizards.loading_screen, wizards.constants, wizards.utils

class ExitScreen(object):

    def __init__(self, player, level_num, came_from):
        super(ExitScreen, self).__init__()
        self.player = player
        self.level_num = level_num
        self.next_level = level_num + 1
        self.player.game_level = self.next_level
        #save player
        self.player.image = None
        print(vars(self.player))

        for item in self.player.inventory:
            item.prepare_to_store()
            print(vars(item))
            #json_string = json.dumps(item, indent=4)
            #print(json_string)

        if os.path.isfile(wizards.constants.PL_FILE):
            os.remove(wizards.constants.PL_FILE)
        # remove images
        for item in self.player.inventory:
            item.image = None

        wizards.utils.save_object(self.player, wizards.constants.PL_FILE)

        #save levels information
        level_information = {}
        if os.path.isfile(wizards.constants.LEVEL_FILE):
            level_information = wizards.utils.load_zip(wizards.constants.LEVEL_FILE)
        level_information[self.level_num] = wizards.constants.NOW

        wizards.utils.save_object(level_information, wizards.constants.LEVEL_FILE)
        wizards.constants.NOW += 1

        self.font = pygame.font.SysFont('Arial', 40)
        self.sfont = pygame.font.SysFont('Arial', 24)

    def render(self, screen):
        screen.fill(BLACK)
        text1 = self.font.render(self.player.name, True, WHITE)
        text2 = self.sfont.render('Press SPACE to continue', True, WHITE)
        text3 = self.sfont.render('Exiting Level ' + str(self.level_num), True, WHITE)
        text4 = self.sfont.render('Experience Gained: ' + str(self.player.xp), True, WHITE)
        text5 = self.sfont.render('Gold Gathered: ' + str(self.player.get_gold_amount()), True, WHITE)
        text7 = self.sfont.render('Speed: ' + str(self.player.stats[self.level_num].speed_percent) + "%", True, WHITE)
        text8 = self.sfont.render('Killed: ' + str(self.player.stats[self.level_num].kills_percent) + "%", True, WHITE)
        text6 = self.sfont.render('Saving Game', True, WHITE)
        screen.blit(text1, (400, 100))
        screen.blit(text3, (400, 150))
        screen.blit(text4, (400, 200))
        screen.blit(text5, (400, 250))
        screen.blit(text6, (400, 300))
        screen.blit(text7, (400, 350))
        screen.blit(text8, (400, 400))
        screen.blit(text2, (400, 450))


    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.manager.go_to(wizards.loading_screen.LoadingScreen(self.next_level))
