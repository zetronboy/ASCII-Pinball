from math import floor, ceil, sqrt
from playfield.pinball_base import PinballElement, PlayfieldIcon, icons
from os import path

class Wall(PinballElement):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.collision_cost = (1.0, 1.0)    
        self.sound = path.join('playfield', 'sounds', 'pop.wav')

class VertWall(Wall):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '|'

    def collide(self, ball) -> tuple:
        speedx, speedy = super().collide(ball) #plays sound and adds points
        # rocoche the x direction and keep the y
        x_inversion = -1
        y_inversion = 1
        angle_cost_to_x = 1 # for horizontal walls: abs(speedx) / ceil(abs(speedx) + abs(speedy))
        angle_cost_to_y = abs(speedy) / ceil(abs(speedx) + abs(speedy)) # 4/4 would be .5 for a 45deg angle
        speedx_cost, speedy_cost = self.collision_cost
        # new_speed = (speedx * -1 * speedx_cost * angle_cost_to_x, speedy * angle_cost_to_y) #if collision_cost is 0, ball stops
        new_speed = (speedx * x_inversion * speedx_cost, speedy * y_inversion * angle_cost_to_y) #if collision_cost is 0, ball stops
        return new_speed
#each control adds itself as a PlayfieldIcon object to the icons list indexed by .pf file symbol
# VertWall constructor is called to create the playfield element when loading the table.
icons['|'] = (PlayfieldIcon('VertWall', '|', VertWall))

class HoriWall(Wall):
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '-'

    def collide(self,ball) -> tuple:        
        speedx, speedy = super().collide(ball) #plays sound and adds points
        # rocoche the x direction and keep the y
        x_inversion = 1
        y_inversion = -1
        angle_cost_to_x = abs(speedx) / ceil(abs(speedx) + abs(speedy))        
        angle_cost_to_y = 1 # for vertical walls: abs(speedy) / ceil(abs(speedx) + abs(speedy)) # 4/4 would be .5 for a 45deg angle
        speedx_cost, speedy_cost = self.collision_cost
        new_speed = (speedx * x_inversion * speedx_cost, speedy * y_inversion * angle_cost_to_y) #if collision_cost is 0, ball stops
        return new_speed

        # rocoche old way
        #x=x, y=x*-1
        # angle is difference between |x| and |y|
        # should be 1 as y approaches 0
        # angle_cost_to_x = abs(speedx) / floor(abs(speedx) +abs(speedy)) 
        # #speed of 4,4 would be .5 (half xspeed) for a 45deg angle hit

        # # need to pass the Ball so we can check its position and adjust
        # if ball.pos[0] < floor(self.game.playfield.width / 2):
        #     adjust_to_move_to_table_center = 1 #push it right
        # elif ball.pos[0] > floor(self.game.playfield.width / 2):
        #     adjust_to_move_to_table_center = -1 #push left
        # # to give the ball a nudge to the center to simulate a sloped surface.

        # speedx_cost, speedy_cost = self.collision_cost
        # new_speed = ((speedx * angle_cost_to_x) + adjust_to_move_to_table_center, 
        #              speedy * -1 * speedy_cost)
        return new_speed
icons['-'] = (PlayfieldIcon('HoriWall', '-', HoriWall))

class BackWall(Wall):
    '''backslash wall'''
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '\\'
        self.points = 100
        self.collision_cost = (0.5,0.5) # scrub speed

    def collide(self,  ball) -> tuple:
        speedx, speedy = super().collide(ball) #plays sound and adds points
        speedx_cost, speedy_cost = self.collision_cost
        # swap x and y movement
        new_speed = (speedy * speedx_cost, speedx * speedy_cost)
        return new_speed
    
icons['\\'] = (PlayfieldIcon('BackWall', '\\', BackWall))

class ForwWall(Wall):
    '''forward slash wall'''
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = '/'
        self.points = 100
        self.collision_cost = (0.5, 0.5) # scrub speed

    def collide(self, ball) -> tuple:
        speedx, speedy = super().collide(ball) #plays sound and adds points
        speedx_cost, speedy_cost = self.collision_cost
        # swap x and y movement        
        inverted = 1
        if speedy > 0:
            inverted = -1 # if ball is moving down: invert, so it travels to the left
        # boost the x bump to get off surfaces
        new_speed = ((speedy + 1) * speedx_cost * inverted, (speedx-1) * speedy_cost)

        return new_speed
    
icons['/'] = (PlayfieldIcon('ForwWall', '/', ForwWall))