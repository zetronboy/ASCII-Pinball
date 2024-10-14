from math import floor, ceil, sqrt
from playfield.pinball_base  import PinballElement, PlayfieldIcon, icons
from os import path
import pygame
import random
class Bumper(PinballElement):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.idle_image = '*'
        self.popped_image = 'O'
        self.image = self.idle_image
        self.collision_cost = (1.1, 1.1) #bouncy
        self.sound = path.join('playfield','sounds','dingsingle.wav')
    
    def collide(self, ball) -> tuple:
        '''return the speed tuple for the ball after it hits this element'''        
        self.image = self.popped_image
        speedx, speedy = super().collide(ball) #plays sound and adds points
        speedx_cost, speedy_cost = self.collision_cost
        #some random velocity for hitting a bumper so it does not always bounce back the way it came
        random_x = random.randrange(75,125) / 100
        random_y = random.randrange(75,125) / 100
        # swap x and y movement
        new_speed = (speedy * speedx_cost * random_x, speedx * speedy_cost * random_y)
        return new_speed
    
    def update(self, tick):
        '''called once per frame'''
        self.image = self.idle_image

icons['*'] = (PlayfieldIcon('bumper', '*', Bumper))
