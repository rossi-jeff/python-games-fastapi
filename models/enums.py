from enum import Enum, IntEnum

class GameStatus(Enum):
    Lost = "Lost"
    Playing = "Playing"
    Won = "Won"

GameStatusArray = ["Lost","Playing","Won"]


class SuitsEnum(IntEnum):
    ONE = 1
    TWO = 2
    FOUR = 4
