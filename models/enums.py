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

class Colors(Enum):
    Black = "Black"
    Blue = "Blue"
    Brown = "Brown"
    Green = "Green"
    Orange = "Orange"
    Purple = "Purple"
    Red = "Red"
    White = "White"
    Yellow = "Yellow"

ColorsArray = ["Black", "Blue", "Brown", "Green", "Orange", "Purple", "Red", "White", "Yellow"]

class Keys(Enum):
    Black = "Black"
    White = "White"

KeysArray = ["Black", "White"]

class Rating(Enum):
    Gray = "Gray"
    Brown = "Brown"
    Green = "Green"

RatingArray = ["Gray","Brown","Green"]
