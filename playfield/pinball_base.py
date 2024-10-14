
from math import floor, ceil, sqrt
from random import random
import pygame

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
        self.sound = None

    def is_colliding(self, ball_position:tuple) -> bool:
        ballx, bally = ball_position
        elmx, elmy = self.pos
        colliding = floor(ballx) == floor(elmx) and floor(bally) == floor(elmy)
        return colliding

    def playsound(self, sound=None):
        if sound:
            pygame.mixer.music.load(sound)
            pygame.mixer.music.play()
        elif self.sound:
            pygame.mixer.music.load(self.sound)
            pygame.mixer.music.play()

    def collide(self, ball) -> tuple:
        '''return the speed tuple for the ball after it hits this element'''
        name_of_class = type(self).__name__
        self.game.add_points_for_hitting(name_of_class)
        self.playsound()
        return ball.speed

    def move(self, x, y):
        self.pos = (x, y)

    def draw(self, display):
        '''update the display with our control image'''
        display.blit(self.pos, self.image) #blit(position_tuple,value):

    def update(self, tick):
        pass
