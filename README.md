# ASCII Pinball

Python3 console pinball game. 
Will prompt for table selection on startup if you have >1 in the playfields folder.


## Building a playfield
Create a [talbename].pf (text) file and a [tablename].json (Javascript Object Notation) file of the same name in the _playfield_ folder. All rows must be the same width (number of columns), but there is no limit on playfield dimesions. 

### Element layout
The [tablename].pf file determines the playfield layout. Draw the table using these symbols for Pinball elements:
ASCII characters | / - \  are walls. You do not supply the outer most playfield wall, it will be built automatically.

^ is the plunger (one supported)

\* are bumpers, they have some springiness like pop bumpers to bounce the ball.

\> is the left flipper. you can have >1 to build a larger flipper like >>>>>. When activated with SHIFT or left/right arrow keys they will add force to ball when contacted (app.py has control binding). Timing is not considered at this time. #ENHANCEMENT

< is the right flipper. You can have >1 like <<<<<<<<<

### JSON score machine
The [tablename].json file determines the score machine. If none provided, it will still work with a default system in code. As the game goes through modes, the score applied by game elements will change. New modes are entered using triggers. Current trigger ability is based on exceeding a number of hits to a elemenet like a bumper. #ENHANCEMENT

The "default" machine is used until one of the machines triggers are reached. The dict includes a "scoring" dict with the name of each control type and its points added when hit. Would have been better to use more specific names for things like Bumper5 but for now its generic. #ENHANCEMENT
"triggers" include optional list with dictionaries "next", and "conditions". The "conditions" dict includes "type" (only hitcount supported for now #ENHANCEMENT), element (generic name matching that used by PlayfieldIcon ), and "hits" for type=hitcount. When the control is hit this many times, the mode will be applied in order built in the file, so put lowest modes first.
Take a look at the example files, or read the Player class.

## Creating new Pinball elements or controls
in the playfield folder are classes for controls. To make a new one, add a new file to this folder and a class that inherits from pinball_base.PinballElement

> from playfield.pinball_base import PinballElement, PlayfieldIcon, icons

Add an icon assigment for your playfield (.pf) design character, for example here is how plunger does it 
> icons['^'] = (PlayfieldIcon('Plunger', '^', Plunger))

The generic name has a number appended to it to create unique control-name when loading playfield. The last parameter Plunger is the class name to instantiate. 

Set your image in the __init__ and call the super().__init__() . The .image is rendered by default.

Optionally impliment collide()
> def collide(self, ball_speed:tuple) -> tuple:

and adjust the ball speed (x,y) when it hits your control. You could put a sound here as well. #ENHANCEMENT

Optionally impliment update()
> def update(self, tick):

To animate your control each frame. tick is fraction of a second the tick is (1/FPS)

## the Ball is the center of the universe
The Ball class does most of the game work. It checks for collisions and calls any hit elements collide() to adjust velocity (speed). 

## Basic code structure
app.py has the main loop; 
* check for input
* update the game
* render the table
* if ball is in the drain, issue another or gameover.

The Game object holds playfield witch has elements dict for the playfield. \
The Game object holds the Players list.

The Players hold their ball count, score, and score_machine used to apply points based on the mode.

## Points mode - score_machine
Pinball is famous for switching the game mode based on goals. when a goal is reached (currently hitting a target x times) the mode advances and the score of each element changes. Then new goals can be reached or you could fall back to lower mode.

This is supported through triggers. I Would like to build this further and make it more sophisticated. #ENHANCEMENT

## Physics - Collision
When the ball hits a wall its velocity (delta-x, delta-y) is adjusted by a modifier. The collide() method will try to simiate bouncing off the surface.

## debugger
Tou can use the keyboard to adjust game parameters angle of the playfield.

___Angle___ can be adjusted in degrees using a or A (shift-a).  Angle is used with gravity to create downward accell. 

___Gravity___ can be adjusted with g or G (shift-g). 

___Friction___ was removed from the game because of complexity, just commented out for now and could add back anytime. The idea was there would be some slowdown traveling accross the playfield laterally. Not sure how valuable it is. Adjusted with f or F.

___Scale___ was removed from the game because it was a crutch early in development. I dont think its still effective. I intended to use to tweak collisions.

## Save game
There is support to serialize the Players into JSON and save /load from disk, like a suspend feature. using Player.loads() to import state and repr(Player) to dump state as JSON. #UNTESTED

## colorized playfield
I would like the elements to show in differnet colors. #ENHANCEMENT

## nudge
Nudge / bump controls have not been added. With the low framerate I don't think its practical. #ENHANCEMENT

## PyGame
Could do a pinball game using Pygame, but need to build some fundamentals without that complexity. Might fork this one day but I would hope to keep the stylistic choice of ASCII based elements in that UI as well. #ENHANCEMENT


# Bugs to fix (keep at bottom of readme, delete as they get fixed)
Collisions can go through walls. The bounce velocity is used to jump the ball one collumn or row in the largest direcection x or y. The test for this is not robust enough.


