
from os import path
import json
from playfield.ball import Ball
from playfield.bumpers import Bumper
from playfield.flippers import LeftFlipper, RightFlipper
from playfield.plunger import Plunger
from playfield.pinball_base import icons
from playfield.walls import VertWall, HoriWall, BackWall, ForwWall

class Playfield:
    '''playfield functions
    load in dict of controls from text playfield design
    '''
    PLAYFIELDS_FOLDER = 'playfields'
    name = ''
    playfield = {}
    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.elements = self.load_playfield_elements(name)
        self.playfield_logic = self.load_playfield_logic(name)
        self.width, self.height = self.get_playfield_dimensions(name)
        
    def __str__(self):
        return self.name
    
    def load_playfield_logic(self, name):
        filename = path.join(self.PLAYFIELDS_FOLDER, name+'.json')
        if path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
            return data
        print("JSON file "+ filename+ " does not exist")    

    def load_playfield_elements(self, name):
        '''build playfield by adding controls 
        returns dict indexed by control name'''
        if '.pf' in name:
            name = name.replace('.pf','')
        print('building', name)
        playfield_controls = {}

        # define playfield controls
        ctrl_counts = {} # indexd by control icon, counts so we can name them individually
        bumper = '*'
        bumper_count = 0
        left_flipper = '>'
        left_flipper_count = 0
        right_flipper = '<'
        right_flipper_count = 0
        plunger = '^'
        vert_wall = '|'
        hori_wall = '-'
        forw_wall = '/'
        back_wall = '\\'
        walls = [vert_wall, hori_wall, forw_wall, back_wall]
        wall_count = 0
        ###########################

        with open(path.join(self.PLAYFIELDS_FOLDER, name +'.pf'), 'r') as pf:
            design = pf.readlines()
            pf.close()
        
        #icons is a dict of objects for controls we can load, indexed by .pf ascii char
        # build top wall, not part of save file
        table_width = len(design[0].strip('\n'))
        horizontal_wall = '-' * table_width
        design = [horizontal_wall] + design  #top  of table added 

        for row_idx, row in enumerate(design):
            row = '|' + row.strip('\n') + '|' #add left and right wall
            for column_idx, pin_elem in enumerate(row):
                if pin_elem in icons.keys(): 
                    ctrl_counts[pin_elem] = ctrl_counts.get(pin_elem, 0) + 1
                    pinball_icon = icons.get(pin_elem)
                    ctrl_name = pinball_icon.name + str(ctrl_counts[pin_elem])
                    playfield_controls[ctrl_name] = pinball_icon.callback(ctrl_name, self.game, column_idx, row_idx)
                elif pin_elem != ' ':
                    print('unrecognized playfield element '+ pin_elem)

        return playfield_controls
    
    def get_playfield_dimensions(self, name):
        '''return a tuple with column count and row count for the passed playfield title'''
        design = []
        row_count = col_count = 0

        with open('playfields/'+ name +'.pf', 'r') as pf:
            design = pf.readlines()
            pf.close()   
        row_count = len(design) + len('-') # add top frame that will be added in load
        if row_count:
            row = design[0].strip('\n')
            col_count = len(row) + len('||') # add the left and right wall that will be added in load
        print('playfield is', row_count, '/', col_count)
        return (col_count, row_count)