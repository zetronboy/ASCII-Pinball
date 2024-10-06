from math import floor, ceil, sqrt
from playfield.pinball_base import PinballElement, PlayfieldIcon, icons

class Wall(PinballElement):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.collision_cost = (1.0, 1.0)    

class VertWall(Wall):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '|'

    def collide(self, ball_speed:tuple) -> tuple:
        speedx, speedy = ball_speed
        # rocoche the x direction and keep the y
        angle_cost_to_y = abs(speedy) / floor(abs(speedx) + abs(speedy)) # 4/4 would be .5 for a 45deg angle
        speedx_cost, speedy_cost = self.collision_cost
        new_speed = (speedx * -1 * speedx_cost, speedy * angle_cost_to_y) #if collision_cost is 0, ball stops
        return new_speed
#each control adds itself as a PlayfieldIcon object to the icons list indexed by .pf file symbol
# VertWall constructor is called to create the playfield element when loading the table.
icons['|'] = (PlayfieldIcon('VertWall', '|', VertWall))

class HoriWall(Wall):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '-'

    def collide(self,ball_speed:tuple) -> tuple:
        speedx, speedy = ball_speed
        # rocoche
        #x=x, y=x*-1
        # angle is difference between |x| and |y|
        # should be 1 as y approaches 0
        angle_cost_to_x = abs(speedx) / floor(abs(speedx) +abs(speedy)) # 4/4 would be .5 for a 45deg angle
        speedx_cost, speedy_cost = self.collision_cost
        new_speed = (speedx * angle_cost_to_x, speedy * -1 * speedy_cost) #if collision_cost is 0, ball stops
        return new_speed
icons['-'] = (PlayfieldIcon('HoriWall', '|', HoriWall))

class BackWall(Wall):
    '''backslash wall'''
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '\\'
        self.points = 100
        self.collision_cost = (0.5,0.5) # scrub speed

    def collide(self,  ball_speed:tuple) -> tuple:
        speedx, speedy = ball_speed       
        speedx_cost, speedy_cost = self.collision_cost
        # swap x and y movement
        new_speed = (speedy * speedx_cost, speedx * speedy_cost)
        return new_speed
    
icons['\\'] = (PlayfieldIcon('BackWall', '|', BackWall))

class ForwWall(Wall):
    '''forward slash wall'''
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '/'
        self.points = 100
        self.collision_cost = (0.5, 0.5) # scrub speed

    def collide(self, ball_speed:tuple) -> tuple:
        speedx, speedy = ball_speed       
        speedx_cost, speedy_cost = self.collision_cost
        # swap x and y movement        
        inverted = 1
        if speedy > 0:
            inverted = -1 # if ball is moving down: invert, so it travels to the left
        # boost the x bump to get off surfaces
        new_speed = ((speedy + 1) * speedx_cost * inverted, (speedx-1) * speedy_cost)
        return new_speed
    
icons['/'] = (PlayfieldIcon('ForwWall', '|', ForwWall))