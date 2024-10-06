from math import floor, ceil, sqrt
from playfield.pinball_base  import PinballElement, PlayfieldIcon, icons
class Bumper(PinballElement):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.idle_image = '*'
        self.popped_image = 'O'
        self.image = self.idle_image
        self.collision_cost = (1.1, 1.1) #bouncy
        #self.points = 200 # poiints come from game.score_mode
        #self.points = self.game.scoremachine[self.name]
    
    def collide(self, ball_speed:tuple) -> tuple:
        '''return the speed tuple for the ball after it hits this element'''        
        self.image = self.popped_image
        speedx, speedy = ball_speed
        speedx_cost, speedy_cost = self.collision_cost
        # swap x and y movement
        new_speed = (speedy * speedx_cost, speedx * speedy_cost)
        return new_speed
    
    def update(self, tick):
        '''called once per frame'''
        self.image = self.idle_image

icons['*'] = (PlayfieldIcon('bumper', '|', Bumper))
