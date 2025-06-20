from enum import Enum

class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    HIT = -1
    MISS = 2
    SUNK = 3