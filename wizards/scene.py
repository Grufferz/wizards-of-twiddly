class Scene:
    
    def __init__(self, director):
        self.director = director
        
    def on_update(self):
        raise NotImplementedError("on_update is abstract")
    
    def handle_events(self, events):
        raise NotImplementedError("handle_events is abstract")
    
    def render(self, screen):
        raise NotImplementedError("render is abstract")
    