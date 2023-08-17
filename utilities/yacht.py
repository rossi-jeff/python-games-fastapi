from typing import List
from .ten_grand import MapDieFaces
from.guess_word import IntListIndex, ListContains
from sqlalchemy.orm import Session
from models.yacht_turn import YachtTurn
from models.enums import YachtCategoryArray, YachtCategory
from payloads.yacht_payload import YachtOption
from models.yacht import Yacht

def ScoreDieNumber(dice: List[int], number: int):
    score = 0
    for d in dice:
        if d == number:
            score = score + number
    return score

def ScoreFullHouse(dice: List[int]):
    score = 0
    _, _, values = MapDieFaces(dice)
    if IntListIndex(3,values) != -1 and IntListIndex(2,values) != -1:
        score = 25
    return score

def ScoreYacht(dice: List[int]):
    score = 0
    _, _, values = MapDieFaces(dice)
    if IntListIndex(5,values) != -1:
        score = 50
    return score

def ScoreLittleStraight(dice: List[int]):
    score = 0
    _, keys, _ = MapDieFaces(dice)
    keys.sort()
    if ",".join(str(k) for k in keys) == "1,2,3,4,5":
        score = 30
    return score

def ScoreBigStraight(dice: List[int]):
    score = 0
    _, keys, _ = MapDieFaces(dice)
    keys.sort()
    if ",".join(str(k) for k in keys) == "2,3,4,5,6":
        score = 30
    return score

def ScoreChoice(dice: List[int]):
    score = 0
    for d in dice:
        score = score + d
    return score

def ScoreFourKind(dice: List[int]):
    score = 0
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] >= 4:
            score = 4 * k
    return score

def YachtSkipCategories(db: Session, id: int):
    skip: List[str] = []
    turns = db.query(YachtTurn).where(YachtTurn.yacht_id == id).all()
    for t in turns:
        if t.Category is not None:
            skip.append(YachtCategoryArray[t.Category])
    return skip

def YachtScoreOptions(dice: List[int], skip: List[str]):
    options: List[YachtOption] = []
    for cat in YachtCategory:
        if len(skip) > 0 and ListContains(cat.name,skip):
            continue
        option = YachtOption(
            Category = cat,
            Score = 0
        )
        if cat.name == "Ones":
            option.Score = ScoreDieNumber(dice,1)
        elif cat.name == "Twos":
            option.Score = ScoreDieNumber(dice,2)
        elif cat.name == "Threes":
            option.Score = ScoreDieNumber(dice,3)
        elif cat.name == "Fours":
            option.Score = ScoreDieNumber(dice,4)
        elif cat.name == "Fives":
            option.Score = ScoreDieNumber(dice,5)
        elif cat.name == "Sixes":
            option.Score = ScoreDieNumber(dice,6)
        elif cat.name == "BigStraight":
            option.Score = ScoreBigStraight(dice)
        elif cat.name == "Choice":
            option.Score = ScoreChoice(dice)
        elif cat.name == "FourOfKind":
            option.Score = ScoreFourKind(dice)
        elif cat.name == "FullHouse":
            option.Score = ScoreFullHouse(dice)
        elif cat.name == "LittleStraight":
            option.Score = ScoreLittleStraight(dice)
        elif cat.name == "Yacht":
            option.Score = ScoreYacht(dice)
        options.append(option)
    options.sort(key=lambda o: o.Score, reverse=True)
    return options

def YachtCategoryScore(cat: YachtCategory, dice: List[int]):
    option = YachtOption(
        Category = cat,
        Score = 0
    )
    if cat.name == "Ones":
        option.Score = ScoreDieNumber(dice,1)
    elif cat.name == "Twos":
        option.Score = ScoreDieNumber(dice,2)
    elif cat.name == "Threes":
        option.Score = ScoreDieNumber(dice,3)
    elif cat.name == "Fours":
        option.Score = ScoreDieNumber(dice,4)
    elif cat.name == "Fives":
        option.Score = ScoreDieNumber(dice,5)
    elif cat.name == "Sixes":
        option.Score = ScoreDieNumber(dice,6)
    elif cat.name == "BigStraight":
        option.Score = ScoreBigStraight(dice)
    elif cat.name == "Choice":
        option.Score = ScoreChoice(dice)
    elif cat.name == "FourOfKind":
        option.Score = ScoreFourKind(dice)
    elif cat.name == "FullHouse":
        option.Score = ScoreFullHouse(dice)
    elif cat.name == "LittleStraight":
        option.Score = ScoreLittleStraight(dice)
    elif cat.name == "Yacht":
        option.Score = ScoreYacht(dice)
    return option.Score

def StringToIntList(string: str, separator: str = ","):
    list: List[int] = (int(i) for i in string.split(separator))
    return list

def UpdateYachtTotal(db: Session, id: int):
    total = 0
    turns = db.query(YachtTurn).where(YachtTurn.yacht_id == id).all()
    for t in turns:
        if t.Score is not None:
            total = total + t.Score
    numTurns = len(turns)
    db.query(Yacht).filter(Yacht.id == id).update({
        "Total": total,
        "NumTurns": numTurns
    })
    db.commit()
  
