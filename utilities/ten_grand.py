from typing import List
from .guess_word import IntListIndex
from models.enums import TenGrandCategory
from payloads.ten_grand_payload import TenGrandScoreOption

def MapDieFaces(dice: List[int]):
    dieMap = {}
    for d in dice:
        if not d in dieMap:
            dieMap[d] = 0
        dieMap[d] = dieMap[d] + 1
    keys: List[int] = []
    for k in dieMap.keys():
        keys.append(k)
    values: List[int] = []
    for v in dieMap.values():
        values.append(v)
    return dieMap, keys, values

def ScoreOnes(dice: List[int]):
    score = 0
    for d in dice:
        if d == 1:
            score = score + 100
    return score

def ScoreFives(dice: List[int]):
    score = 0
    for d in dice:
        if d == 5:
            score = score + 50
    return score

def ScoreFullHouse(dice: List[int]):
    score = 0
    _, _, values = MapDieFaces(dice)
    if IntListIndex(3,values) != -1 and IntListIndex(2,values) != -1:
        score = 1500
    return score

def ScoreStraight(dice: List[int]):
    score = 0
    _, keys, _ = MapDieFaces(dice)
    keys.sort()
    if ",".join(str(k) for k in keys) == "1,2,3,4,5,6":
        score = 2000
    return score

def ScoreThreePair(dice: List[int]):
    score = 0
    _, _, values = MapDieFaces(dice)
    if ",".join(str(v) for v in values) == "2,2,2":
        score = 1500
    return score

def ScoreDoubleThreeKind(dice: List[int]):
    score = 0
    _, keys, values = MapDieFaces(dice)
    if ",".join(str(v) for v in values) == "3,3":
        for k in keys:
            if k == 1:
                score = score + 1000
            else:
                score = score + (k * 100)
    return score

def ScoreThreeKind(dice: List[int]):
    score = 0
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 3:
            if k == 1:
                score = score + 1000
            else:
                score = score + (k * 100)
    return score

def ScoreFourKind(dice: List[int]):
    score = 0
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 4:
            if k == 1:
                score = score + 2000
            else:
                score = score + (k * 200)
    return score

def ScoreFiveKind(dice: List[int]):
    score = 0
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 5:
            if k == 1:
                score = score + 4000
            else:
                score = score + (k * 400)
    return score

def ScoreSixKind(dice: List[int]):
    score = 0
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 6:
            if k == 1:
                score = score + 8000
            else:
                score = score + (k * 800)
    return score

def TenGrandScoreOptions(dice: List[int]):
    Options: List[TenGrandScoreOption] = []
    for cat in TenGrandCategory:
        option = TenGrandScoreOption(
            Score = 0,
            Category = cat
        )
        if cat.name == "Ones":
            option.Score = ScoreOnes(dice)
        elif cat.name == "Fives":
            option.Score = ScoreFives(dice)
        elif cat.name == "ThreePairs":
            option.Score = ScoreThreePair(dice)
        elif cat.name == "Straight":
            option.Score = ScoreStraight(dice)
        elif cat.name == "FullHouse":
            option.Score = ScoreFullHouse(dice)
        elif cat.name == "DoubleThreeKind":
            option.Score = ScoreDoubleThreeKind(dice)
        elif cat.name == "ThreeKind":
            option.Score = ScoreThreeKind(dice)
        elif cat.name == "FourKind":
            option.Score = ScoreFourKind(dice)
        elif cat.name == "FiveKind":
            option.Score = ScoreFiveKind(dice)
        elif cat.name == "SixKind":
            option.Score = ScoreSixKind(dice)
        
        if option.Score > 0 or option.Category == TenGrandCategory.CrapOut:
            Options.append(option)
    Options.sort(key=lambda o: o.Score, reverse=True)
    return Options
