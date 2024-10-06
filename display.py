'''renders the playfield to the terminal'''
from math import floor,ceil

#from colorama import init,just_fix_windows_console,Fore,Back,Style
class Display:
    rows = []
    def __init__(self,width,height, game):
        self.set_mode(width,height)
        self.game = game
        #just_fix_windows_console() #colorama needs an import with PIP
        #init(autoreset=True)


    def draw(self):
        '''render'''
        print( chr(27) + "[2J") # HOME ANSI ESC CODE
        print( chr(27) + "[H") #move to home position
        width = 0
        #top line
        if len(self.rows):
            width = len(self.rows[0])
            self.draw_horizontal_line('_', width)
            self.draw_score(width)
            self.draw_horizontal_line('-', width)
        for row in self.rows:
            print("|", "".join(row), "|", sep='')
        #bottom line
        for _ in range(width+2):
            print("-",end='')
        
        self.draw_debug()

    def draw_debug(self):  
        ball = self.game.playfield.elements.get('ball1')      
        ball_speed = (round(ball.speed[0],1), round(ball.speed[1],1))
        ball_pos = (round(ball.pos[0],1), round(ball.pos[1],1))
        print('\n(a)ngle=', self.game.playfield_angle, '(f)riction=', self.game.playfield_friction, '(g)ravity=', self.game.gravity, '(s)cale=', self.game.scale,'ball_speed=', str(ball_speed), 'ball_pos=', str(ball_pos))

    def draw_horizontal_line(self, char, width):
        for _ in range(width + 2):
            print(char,end='')
        print()

    def draw_score(self, width):
        print(self.game.current_player)
        # score = self.game.score
        # ball = self.game.ball     
        # dmd = "Ball: {:d} P1: {:5d}".format(ball, score)
        # padding = width - len(dmd) - len('  ') #width does not include sides of table||
        # spacer = " " * padding
        # print('| '+ dmd + spacer +' |')
    def blit(self, position_tuple,value):
        col, row = position_tuple # (x,y)
        if col >=0 and col <= self.game.playfield.width and row >=0 and row <= self.game.playfield.height:
            self.rows[floor(row)][floor(col)] = value
        else:
            print('out of bounds in display')
            
    def set_mode(self, width, height):
        '''clears and rebuilds the playfield as 2dim array'''
        self.rows = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(' ')
            self.rows.append(row)

