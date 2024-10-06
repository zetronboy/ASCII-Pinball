from enum import Enum
class states(Enum):
    IDLE = 0
    ACTIVE = 1
    INSHOE = 2 #waiting launch
    INPLAY = 3
    INGUTTER = 4
    OVER = 5

class PlayerStates:
    WAITING = 0
    ACTIVE = 1
    GAMEOVER = 2