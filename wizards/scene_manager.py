from wizards.title_screen import *

class SceneManager(object):
    
    def __init__(self):
        self.go_to(TitleScreen())
        
    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self