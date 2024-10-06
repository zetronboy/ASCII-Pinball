from playfield.pinball_base import PinballElement, PlayfieldIcon, icons
from gamestates import states

class Plunger(PinballElement):
    MAX_PLUNGER_DRAW = 50 # how far you can pull back the plunger, blocks per second
    PLUNGER_DRAW_SPEED = 4 # pull force per frame
    pulled_plunger = ':'
    idle_plunger = '^'
    def __init__(self, name, game, x, y):
        super().__init__(name, game, x, y)
        self.image = self.idle_plunger
        self.plunger_draw = 0        

    def pull(self, game, pulling):
        '''pulling plunger'''
        if not pulling and self.plunger_draw > 0:
            self.launch(game)
            return
        if pulling:
            self.plunger_draw += self.PLUNGER_DRAW_SPEED
        else:
            self.plunger_draw = 0

    def update(self, tick):
        #if self.plunger_draw > self.MAX_PLUNGER_DRAW:
            #print(self.plunger_draw)
            #self.launch(self.game)
        if self.plunger_draw > 0:
            self.image = self.pulled_plunger
        else:
            self.image = self.idle_plunger

    def launch(self, game):
        if game.state == states.INSHOE:
            print('launch the ball')
            ball = game.playfield.elements.get('ball1')
            if ball:
                ball.speed = (0.0, self.plunger_draw*-1) #ball goes up
            self.plunger_draw = 0
            game.state = states.INPLAY

    def collide(self, ballspeed):
        self.game.state == states.INSHOE
        return super().collide(ballspeed)

icons['^'] = (PlayfieldIcon('plunger', '|', Plunger))