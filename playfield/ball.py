from math import floor, ceil, sqrt
from playfield.pinball_base import PinballElement, PlayfieldIcon, icons
from gamestates import states

class Ball(PinballElement):
    MOVEMENT_PRECISION = 0.1 # we can move 1/10th of a character but render to a whole char
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = 'O'
    
    def update(self, tick):
        '''move the ball based on forces and previous velocity
        * tick: fraction of a second like 0.25 to render 1/4 sec of updates'''
        if self.game.state != states.INPLAY:
            return
        
        speed_x, speed_y = self.speed #tuple 
        pos_x, pos_y = self.pos
        #lower the playfield angle, the slower the ball will accell to the bottom
        #  when angle is 90, accell is just gravity. lower angles reduce this linear (should be exponent i think)
        linear = (self.game.playfield_angle / 90.0)
        accell_y = linear * self.game.gravity * self.game.scale #pos accell is down
        speed_y = speed_y + accell_y

        #apply some surface drag
        # if speed_y > 0: #moving down
        #     speed_y -= (speed_y * game.playfield_friction)  #portion of your speed lost to friction
        # elif speed_y < 0:
        #     speed_y -= (speed_y * game.playfield_friction )  # subtract negative speed to get positive adjustment
        travel_y = speed_y * tick

        # if speed_x > 0: #moving right
        #     speed_x -= speed_x * game.playfield_friction 
        # elif speed_x < 0:
        #     speed_x -= speed_x * game.playfield_friction            
        travel_x = speed_x * tick

        self.speed = (speed_x, speed_y) # tenth of a frame precision
        self.move(dest_x=pos_x + travel_x, 
                  dest_y=pos_y + travel_y)
        if self.is_out_of_bounds(): # bottom of the playfield
            self.game.state = states.INGUTTER

    def move(self, dest_x, dest_y):
        '''move and check collision
        coordinate system has 0 at top left corner
        if the ball is to move>1 space, move it one space at a time and check for collision like casting a ray
        '''
        if dest_y > 20:
            print('break')
        #newx, newy = self.pos
        current_x, current_y = self.pos    
        out_of_bounds = False
        while (current_x != dest_x or current_y != dest_y and out_of_bounds == False):
            if current_x < dest_x:        
                if dest_x - current_x > 1:
                    current_x += 1.0 # if more than 1 block away, move a block at a time so we can test collision
                else:
                    current_x = dest_x # if within a block, just set the new location 

            elif current_x > dest_x:
                if current_x - dest_x > 1:
                    current_x -= 1.0
                else:
                    current_x = dest_x

            if current_y < dest_y:
                if dest_y - current_y > 1:
                    current_y += 1
                else:
                    current_y = dest_y

            elif current_y > dest_y:            
                if current_y - dest_y > 1:
                    current_y -= 1
                else:
                    current_y = dest_y

            colliding = self.get_colliding_elements((current_x, current_y))
            if colliding:                    
                self.speed = colliding[0].collide(self) # bound off element, 
                # each element adds their own points, makes a sound, and adjusts ball speed on collide()
                self.push_ball_off_colliding_elements(colliding)
                
                return   

            self.pos = (current_x, current_y)

            out_of_bounds = self.is_out_of_bounds()

    def push_ball_off_colliding_elements(self, colliding_elements):
        '''use our momentum and shift 1 cell that direction'''
        dx, dy = self.speed
        x, y = self.pos
        if abs(dx) > abs(dy): #moving horizontally more than vertically
            if dx > 0:
                x = floor(x) +1
            elif dx < 0: 
                x = floor(x) -1
            self.pos = (x,y)
        else: #moving more vertically than horizontally
            if dy > 0:
                y = floor(y) +1
            elif dy < 0:#could be standing still like when sitting on plunger
                y = floor(y) -1
            self.pos = (x,y)

    def is_out_of_bounds(self):
        x, y = self.pos
        if y > self.game.playfield.height or x < 0 or y < 0 or x > self.game.playfield.width:
            return True
        return False


    def is_colliding(self, position=None) -> bool:
        colliding = False
        if position is None: #if they don't pass a test position, check the current position
            position = self.pos 
        for name, element in self.game.playfield.elements.items():
            if element != self:
                if element.is_colliding(position) :
                    colliding = True                    
        return colliding

    def get_colliding_elements(self, position=None) -> PinballElement:
        '''returns list of colliding game elements at position
        or empty list if none'''
        colliding_elements = []
        if position is None: #if they don't pass a test position, check the current position
            position = self.pos 
        for name, element in self.game.playfield.elements.items():
            if element != self:
                if element.is_colliding(position) :
                    colliding_elements.append(element)
        return colliding_elements

icons['O'] = (PlayfieldIcon('Ball', 'O', Ball))



