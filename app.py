#!/usr/bin/python3
'''Pinball console
play pinball in terminal/shell
Author: Joey Collard 2024'''
#REF https://www.ipdb.org/glossary.php

from time import sleep
import pygame
import keyboard
from os import path, listdir

from display import Display
from game import PinballGame, states
#from playfield.loader import get_playfield_dimensions,load_playfield_elements

FRAMERATE = 24 #FPS
pygame.init()
#screen = pygame.display.set_mode((820, 1024))
#clock = pygame.time.Clock()
def main():
    playfield_name = get_playfield_choice() # like a main menu
    #print("starting "+ playfield_name)
    #elements = load_playfield_elements(playfield_name) #plunger, bumpers, flippers and so on
    #playfield_width, playfield_height = get_playfield_dimensions(playfield_name)
    
    #
    # todo: load saved game from disk 
    #
    save_game_filename = None # could load a paused game and pass it to the game to continue where you left off

    game = PinballGame(playfield_name)
    if save_game_filename:
        game.load(save_game_filename)
    game.start(players=1, balls=3)
    while (game.state != states.OVER):
        if game.state == states.INGUTTER:
            game.advance_player()
            if game.current_player.ball < game.current_player.balls:
                game.new_ball()
            else:
                break #game over
        check_input(game)
        update(game)
        if game.state == states.INPLAY or game.state== states.INSHOE:
            render(game)
            sleep(1 / FRAMERATE)
    print("GAME OVER")
    game.save('savegame')

def get_playfield_choice():
    choices = []
    choice = None
    for file in listdir('playfields'):
        if file.endswith('.pf'):
            choices.append(file.replace('.pf',''))
    if len(choices) == 1:
        return choices[0]
    
    while True:        
        print( chr(27) + "[2J") # HOME ANSI ESC CODE
        print('','Select a playfield from below')
        for index, choice in enumerate(choices):
            print(str(index +1) +') '+ choice)

        selection = input('choice or Q to quit\n')
        if selection.lower().startswith('q'):
            exit()
        if int(selection) <= len(choices):
            return choices[int(selection) -1]

def check_input(game):
    '''look for keyboard mouse joystick inputs and act
    accept debug inputs for adjusting physics in-game
    '''
    elements = game.playfield.elements
    # Wait for the next event. does not require pygame
    # https://github.com/boppreh/keyboard#api
    isleft = keyboard.is_pressed('left')
    isright = keyboard.is_pressed('right')
    isdown = keyboard.is_pressed('down')
    lshift_pressed = keyboard.is_pressed('left shift')
    rshift_pressed = keyboard.is_pressed('right shift')

    qpressed = keyboard.is_pressed('q')

    left_flippers = []
    for name, element in elements.items():
        if name.lower().startswith('lflipper'):            
            element.set(isleft or lshift_pressed)
        if name.lower().startswith('rflipper'):
            element.set(isright or rshift_pressed)
            
    plunger = elements.get('Plunger1') #only supports 1 plunger, ATM..
    assert plunger is not None
    plunger.pull(game, isdown)

        

    if game.DEBUG:
        apressed = keyboard.is_pressed('a') #angle
        Apressed = keyboard.is_pressed('SHIFT+a')
        fpressed = keyboard.is_pressed('f') #friction
        Fpressed = keyboard.is_pressed('SHIFT+f')
        
        gpressed = keyboard.is_pressed('g') #graivty
        Gpressed = keyboard.is_pressed('SHIFT+g')
        spressed = keyboard.is_pressed('s') #scale
        Spressed = keyboard.is_pressed('SHIFT+s')

        if Apressed: #check caps first
            game.playfield_angle -= 1
            if game.playfield_angle < 1:
                game.playfield_angle = 1
        elif apressed:
            game.playfield_angle += 1
            if game.playfield_angle > 45:
                game.playfield_angle = 45

        if Fpressed:
            game.playfield_friction -= 0.1
            if game.playfield_friction < 0.1:
                game.playfield_friction = 0.1
        elif fpressed:
            game.playfield_friction += 0.1
            if game.playfield_friction > 1.0:
                game.playfield_friction = 1.0
        
        if Gpressed: #check caps first
            game.gravity -= 1
            if game.gravity < 1:
                game.gravity = 1
        elif gpressed:
            game.gravity += 1
            if game.gravity > 45:
                game.gravity = 45

        if Spressed: #magic number
            game.scale -= 1
            if game.scale < 1:
                game.scale = 1
        elif spressed:
            game.scale += 1
            if game.scale > 99:
                game.scale = 99

    if qpressed:
        game.state = states.OVER

    #this could be used after we switch to pygame.
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_a]: #left flipper
    #     print('left')
    # elif keys[pygame.K_RIGHT]:
    #     print('right')
    # elif keys[pygame.K_DOWN]:
    #     print('down')
    # # maybe space for nudge

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.KEYDOWN:
    #         print(event.key, event.mod, event.unicode, event.scancode)

def update(game):
    '''have each control update their position and state and animation'''
    game_elements = game.playfield.elements
    for key, control in game_elements.items():
        control.update(1 / FRAMERATE)
    

def render(game):
    '''create a new window and render each element like bumpers onto playfield'''
    game_elements = game.playfield.elements
    disp = Display(game.playfield.width, game.playfield.height, game)    
    for key, control in game_elements.items():
        control.draw(disp)       
    disp.draw()
    sleep(1/FRAMERATE) # temp

if __name__ == "__main__":
    main()