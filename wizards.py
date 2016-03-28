
import pygame, random
from wizards import *

def main():
    pygame.init()
    random.seed()
    screen = pygame.display.set_mode(constants.SCREENSIZE)
    timer = pygame.time.Clock()
    pygame.display.set_caption("The Wizards Of Twiddly")
    running = True
    
    manager = scene_manager.SceneManager()
    
    while running:
        timer.tick(60)
                          
        if pygame.event.get(pygame.QUIT):
            running = False
            return
        manager.scene.handle_events(pygame.event.get()) 
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
        
    
if __name__ == '__main__':
    main()
    pygame.quit()