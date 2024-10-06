
import json

from playfield.ball import Ball
from playfield.playfield import Playfield
from player import Player

from gamestates import states


class PinballGame:
    scale = 1
    gravity = 25
    playfield_angle = 6.0 # deg
    playfield_friction = 0.5 # drag to deaccell the ball, 1.0=no drag, 0.1=lots of drag 1/10 speed
    bounce_cost = 0.1 #slow down when bouncing off an element like wall, flipper and bumper will add accell
    
    #functions to change the state

    def launch_ball(self):
        '''send ball into field, random hit an element'''
        self.state = states.INPLAY
    def gutter_ball(self):
        self.state = states.INGUTTER
    def game_over(self):
        self.state = states.OVER
    state = states.IDLE
    
    def __init__(self, playfield_name):
        '''
        * playfield_name: a table .pf and .json withe the same name will be loaded'''
        self.playfield = Playfield(playfield_name, self) #holds elements and playfield_logic
        self.players = []
        self.current_player = None
        
    def __repr__(self):
        return { 
            'playfield': str(self.playfield), 
            'players': repr(self.players)
            }
    
    def load(self, filename):
        '''pass dict you got file savefile, created by save()'''
        initial_game_state = json.load(filename)
        if initial_game_state.get('playfield') != self.playfield.name:
            assert ValueError("attempting to load save data for a different playfield")
        for player in initial_game_state.get('players'):
            self.add_player(repr_dict=player)

    def save(self, filename):
        save_content = repr(self)
        with open(filename, 'w') as file:
            file.write(save_content)

    def start(self, players, balls=3):    
        self.state = states.ACTIVE
        for player in range(1,int(players)+1):
            self.add_player("Player"+ str(player))
        assert len(self.players) > 0
        self.set_player(1) #1 indexed
        self.new_ball()

    def set_player(self, name_or_number):
        '''1s based player number, or their name'''
        if isinstance(name_or_number, int) or name_or_number.isnumeric():
            self.current_player = self.players[int(name_or_number)-1]
        else:
            self.current_player = self.players.get(name_or_number)

    def advance_player(self):
        '''move to the next player'''
        for index, player in enumerate(self.players):
            if player == self.current_player:
                current_index = index
                new_index = current_index +1
                if new_index >= len(self.players):
                    new_index = 0
        self.current_player = self.players[new_index]

    def add_player(self, name='', balls=3, repr_dict=None):
        new_player = Player(self, name, balls)
        if repr_dict:
            new_player.loads(repr_dict)
            new_player.load_score_modes(self.playfield.playfield_logic.copy())
            #make sure this is a copy of the playfield logic, 
            # it controls how scoring is applied in each mode of play
        self.players.append(new_player)

    def new_ball(self):
        '''set initial ball position above plunge'''
        assert self.current_player.ball < self.current_player.balls            
        for name, elem in self.playfield.elements.items():
            if 'plunger' in elem.name:
                plungerx, plungery = elem.pos                
                self.playfield.elements['ball1'] = Ball('ball1', self, plungerx, plungery - 1)
                self.current_player.new_ball() #state machine controls scoring based on game state
                self.state = states.INSHOE
                break