'''renders the playfield to the terminal'''
from math import floor,ceil

from colorama import init,just_fix_windows_console,Fore,Back,Style
just_fix_windows_console()

class Display:
    border_color = Fore.BLUE
    playfield_color = Fore.GREEN
    score_color = Fore.RED
    debug_color = Fore.BLACK 

    rows = [] # model of playfield as rows of character column
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
            #self.draw_horizontal_line('-', width)
        for row in self.rows:
            print(self.border_color + "|", self.playfield_color + "".join(row), self.border_color + "|", sep='')
        #bottom line
        self.draw_horizontal_line('-', width)
        
        if self.game.DEBUG:
            self.draw_debug()

    def draw_debug(self):
        ball = self.game.playfield.elements.get('ball1')      
        ball_speed = (round(ball.speed[0],1), round(ball.speed[1],1))
        ball_pos = (round(ball.pos[0],1), round(ball.pos[1],1))
        print(self.debug_color + '\n(a)ngle=', self.game.playfield_angle, '(f)riction=', self.game.playfield_friction, '(g)ravity=', self.game.gravity, '(s)cale=', self.game.scale,'ball_speed=', str(ball_speed), 'ball_pos=', str(ball_pos))

    def draw_horizontal_line(self, char, width):
        line = ''.join([char for _ in range(width + 2)]) 
        # equivilent"
        # for _ in range(width + 2):
        #     line += char
        print(self.border_color + line)

    def draw_score(self, width):
        player_display = str(self.game.current_player)
        left_padding = " " * int( ( self.width - len(player_display)) / 2)
        right_padding = " " * int( self.width - len(left_padding) - len(player_display))
        print(self.border_color + "|" + left_padding + self.score_color  + player_display + right_padding + self.border_color + "|")

    def blit(self, position_tuple,value):
        col, row = position_tuple # (x,y)
        if col >=0 and col <= self.game.playfield.width and row >=0 and row <= self.game.playfield.height:
            self.rows[floor(row)][floor(col)] = value
        else:
            print('out of bounds in display')
            
    def set_mode(self, width, height):
        '''clears and rebuilds the playfield as 2dim array'''
        self.width = width
        self.height = height
        self.rows = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(' ')
            self.rows.append(row)

