
from math import floor, ceil, sqrt
from random import random

icons = {} #.pf playfield map file representation of control
class PlayfieldIcon:
    '''access the class using the playfield icon for that element/control
    used to construct playfield from pf files. from '/' you can find the constructor for the forward wall.'''
    def __init__(self, name, pf_symbol, class_ref ):
        self.name = name
        self.symbol = pf_symbol
        self.callback = class_ref

class PinballElement():
    def __init__(self, name, game, x=None, y=None):
        self.name = name
        self.game = game
        self.pos = (x, y) #position
        self.speed:tuple[float,float] = (0.0, 0.0) 
        self.points = 0 # when hit add to score
        self.collision_cost = (0.0,0.0) # ball speed is multiplied by this when it collides with an element
        #self.ricoche = False # bounce at an angle, used for angled walls and flippers?

    def is_colliding(self, ball_position:tuple) -> bool:
        ballx, bally = ball_position
        elmx, elmy = self.pos
        colliding = floor(ballx) == floor(elmx) and floor(bally) == floor(elmy)
        if colliding:
            print("collision with "+ str(self))
        return colliding

    def collide(self, ball_speed:tuple) -> tuple:
        '''return the speed tuple for the ball after it hits this element'''
        speedx, speedy = ball_speed
        speedx_cost, speedy_cost = self.collision_cost #adjust for the collision
        #random_factor = random() # 0-1
        new_speed = (speedx * -1 * speedx_cost , speedy * -1 * speedy_cost ) #if collision_cost is 0, ball stops
        return new_speed

    def move(self, x, y):
        self.pos = (x, y)

    def draw(self, display):
        '''update the display with our control image'''
        display.blit(self.pos, self.image) #blit(position_tuple,value):

    def update(self, tick):
        pass
