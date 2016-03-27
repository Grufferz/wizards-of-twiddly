import random 

class FireEffect(object):
    
    def __init__(self, r):
        self.resistance = r
        
        
class Heat(object):
    
    def __init__(self, i, r):
        self.intensity = i
        self.radius = r
        
        
        
        
        
class BlankObject(object):
    
    def __init__(self, fire=None, heat=None):
        self.x = 0
        self.y = 0
        self.name = "Blank"
        self.fire_effect = fire
        self.heat = heat
        self.flammable = False
        
    def set_position(self,x,y):
        self.x = x
        self.y = y
        

class TreeWood(BlankObject):
    
    def __init__(self, x, y,fire=None, heat=None):
        BlankObject.__init__(self,fire,heat)
        self.x = x
        self.y = y
        self.name = "Tree"
        self.flammable = True
        

class BurningTree(BlankObject):
    
    def __init__(self, x, y,fire=None, heat=None):
        BlankObject.__init__(self,fire,heat)
        self.x = x
        self.y = y
        self.name = "Burning Tree"
        self.flammable = False
        