
from dataclasses import dataclass
from gamestates import states, PlayerStates



# dataclass adds functions like repr and str without any work
@dataclass
class Player():
    name: str
    hitcounts: dict
    score: int=0
    multiplier: int=0
    ball: int=0
    balls: int=3    
    score_mode_name: str="default" #changes scoring applied and moves score_state
    state: PlayerStates=PlayerStates.WAITING

    def __init__(self, game, name='', balls=3):
        self.game = game
        self.name = name
        self.balls = balls
        #self.scoreboard = ScoreMachine()

        # set the scores for each control, default has just one state
        # replaced when load called, below is a placholder to understand structure
        self.load_score_modes( { "default": {
                "scoring": {
                    "VertWall": 0,
                    "HoriWall": 0,
                    "ForwWall": 0,
                    "BackWall": 0,
                    "Plunger": 0,
                    "Bumper": 200,
                    "LeftFlipper": 0,
                    "RightFlipper": 0,
                    "Ball": 0
                    },
                "triggers": [],
                "description": "default scoring"
                }
            })
        self.set_mode("default")
        # one dict for each player, can be serialized to save/load as json
        self.hitcounts = {} # counts with each playfield element the player has hit
        self.score = 0
        self.multiplier = 0

    def __str__(self) -> str:
        '''used as the Dot Matrix Display representation of our score'''
        width = self.game.playfield.width        
        dmd = "{:s} Ball: {:d}/{:d} {:5d}".format(self.name, self.ball, self.balls,  self.score)
        padding = width - len(dmd) - len('  ') #width does not include sides of table||
        spacer = " " * padding
        return '| '+ dmd + ' '+ self.score_mode.get('description') +' |'
    
    def loads(self, repr_dict):
        '''set all paramters based on a passed dict that was the result of repr() of our dataclass'''
        self.name = repr_dict.get('name','')
        self.score = repr_dict.get('score',0)
        self.multiplier = repr_dict.get('multiplier',0)
        self.ball = repr_dict.get('ball')
        self.balls = repr_dict.get('balls')
        
        assert self.score_mode != None # the modes should have been loaded before calling
        self.set_mode( repr_dict.get('mode','default') )
        self.hitcounts = repr_dict.get('hitcounts')
    
    # def __repr__(self) -> str:
    #     '''used in file save to create JSON gamestate'''
    #     return { 
    #         "name": self.name,
    #         "score": self.score,
    #         "multiplier": self.multiplier,
    #         "mode": self.current_mode, 
    #         "hitcounts": self.hitcounts,
    #         }    

    def load_score_modes(self, machine_dict):
        '''takes a dictionary of machine states that includes scoring dict and description'''
        if isinstance(machine_dict, dict):
            self.score_modes = machine_dict
            return True
        assert ValueError("load_score_modes expected a dictionary")

    def set_mode(self, mode_name):
        if not mode_name:
            assert ValueError("set_mode expected mode, got None")
        if self.score_modes.get(mode_name):
            self.score_mode_name = mode_name
            self.score_mode = self.score_modes.get(mode_name)
            return
        self.score_mode = 'default'
        raise ValueError("score machine set_mode could not find the passed mode "+ mode_name)
    
    def add_points(self, element_name):
        '''use the state to add points and possibly trigger a new state
        call this when a target is hit by the ball.'''
        points = self.get_points(element_name)
        self.score += points
        hit_counter = self.hitcounts.get(element_name)
        if hit_counter is not None:
            self.hitcounts[element_name] = int(hit_counter) +1
        else:
            self.hitcounts[element_name] = 1
        self.apply_triggers(element_name)

    def apply_triggers(self, element_name):
        '''check for triggers and change score state state'''
        # EXAMPLE TRIGGER
        # { 
        #         "next": "two", 
        #         "type": "hitcount",
        #         "element": "Bumper", 
        #         "hits": 1  
        #     }
        machine = self.score_mode #returns dict
        triggers = machine.get('triggers') # each trigger looks like this "Bumper": { "hits": 1, "next": "two" }
        
        for trigger_dict in triggers: #check all the triggers    
            conditions_passing = True            
            next_mode = trigger_dict.get('next')
            type = trigger_dict.get('type') # hitcount
            element = trigger_dict.get('element')                
            if type == 'hitcount':
                hits = trigger_dict.get('hits', 0)
                if self.hitcounts.get(element, 0) < int(hits):
                    conditions_passing = False
            #other conditional tests would go here

            # if the mode trigger is satisfied, and identifies a next mode, switch to it
            if conditions_passing and next_mode:
                self.set_mode( next_mode )


    def get_points(self, element_name):
        '''returns points for the passed Pinball element based on the state.
        used by add_points()'''
    
        if not  self.score_mode:
            print("failed to find a scoring system for the current machine state, using default")
            self.set_mode('default')

        scoring =  self.score_mode.get('scoring')
        if scoring:
            #print("loaded scoring for state "+  self.score_mode.get('description', 'unknown'))
            return int(scoring.get(element_name))
        print("error getting scoring")
        return 0
    
    def new_ball(self):
        current_ball = self.ball
        new_ball = current_ball + 1
        if new_ball > self.balls:
            self.gameover()
        else:
            self.ball = new_ball
            self.state = PlayerStates.ACTIVE

    def gameover(self):
        self.state = PlayerStates.GAMEOVER