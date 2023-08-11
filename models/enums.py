from enum import Enum

class GameStatus(str,Enum):
    Lost = "Lost"
    Playing = "Playing"
    Won = "Won"

GameStatusArray = ["Lost","Playing","Won"]
