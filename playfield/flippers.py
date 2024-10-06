from math import floor, ceil, sqrt
from playfield.pinball_base import PinballElement, PlayfieldIcon, icons
class Flipper(PinballElement):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.idle_image = '?'
        self.flipped_image = '-'
        self.image = self.idle_image        
        self.flipper_power = (5.0, 5.0) #when a ball is hit, gets this speed boost
        
    def isflipped(self):
        return self.image == self.flipped_image
    

class LeftFlipper(Flipper):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x,y)
        self.idle_image = '>'
        self.flipped_image = '/'
        self.image = self.idle_image
        self.flipper_power = (-2, 5)
    
    def set(self, state):
        '''sets flipper state
        * state: if not False/None/0, then the flipper is set'''        
        if state:
            self.image = self.flipped_image
            self.collision_cost = self.flipper_power
        else:
            self.image = self.idle_image
            self.collision_cost = (1.0, 0.0)
icons['>'] = (PlayfieldIcon('lflipper', '|', LeftFlipper))

class RightFlipper(Flipper):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.idle_image = '<'
        self.image = self.idle_image
        self.flipped_image = '\\'

    def set(self, state):
        '''sets flipper state
        * state: if not False/None/0, then the flipper is set'''        
        if state:
            self.image = self.flipped_image
            self.collision_cost = self.flipper_power
        else:
            self.image = self.idle_image
            self.collision_cost = (1.0,0.0)
icons['<'] = (PlayfieldIcon('rflipper', '|', RightFlipper))