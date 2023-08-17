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

class ShipType(Enum):
    BattleShip = "BattleShip"
    Carrier = "Carrier"
    Cruiser = "Cruiser"
    PatrolBoat = "PatrolBoat"
    SubMarine = "SubMarine"
    
ShipTypeArray = ["BattleShip","Carrier","Cruiser","PatrolBoat","SubMarine"]

ShipTypeSize = {"BattleShip": 4,"Carrier": 5,"Cruiser": 3,"PatrolBoat": 2,"SubMarine": 3}

class Navy(Enum):
    Player = "Player"
    Opponent = "Opponent"

NavyArray = ["Player","Opponent"]

class Target(Enum):
    Miss = "Miss"
    Hit = "Hit"
    Sunk = "Sunk"

TargetArray = ["Miss","Hit","Sunk"]

class TenGrandCategory(Enum):
    CrapOut = "CrapOut"
    Ones = "Ones"
    Fives = "Fives"
    ThreePairs = "ThreePairs"
    Straight = "Straight"
    FullHouse = "FullHouse"
    DoubleThreeKind = "DoubleThreeKind"
    ThreeKind = "ThreeKind"
    FourKind = "FourKind"
    FiveKind = "FiveKind"
    SixKind = "SixKind"

TenGrandCategoryArray = [
    "CrapOut", "Ones", "Fives", "ThreePairs", "Straight", 
    "FullHouse", "DoubleThreeKind", "ThreeKind", "FourKind", 
    "FiveKind", "SixKind"
]

TenGrandDiceRequired = {
    "CrapOut": 0, 
    "Ones": 1, 
    "Fives": 1, 
    "ThreePairs": 6, 
    "Straight": 8, 
    "FullHouse": 5, 
    "DoubleThreeKind": 6, 
    "ThreeKind": 3, 
    "FourKind": 4, 
    "FiveKind": 5, 
    "SixKind": 6
}

class YachtCategory(Enum):
    BigStraight = "BigStraight"
    Choice = "Choice"
    Fives = "Fives"
    FourOfKind = "FourOfKind"
    Fours = "Fours"
    FullHouse = "FullHouse"
    LittleStraight = "LittleStraight"
    Ones = "Ones"
    Sixes = "Sixes"
    Threes = "Threes"
    Twos = "Twos"
    Yacht = "Yacht"

YachtCategoryArray = ["BigStraight", "Choice", "Fives", "FourOfKind", "Fours", "FullHouse", "LittleStraight", "Ones", "Sixes", "Threes", "Twos", "Yacht"]
