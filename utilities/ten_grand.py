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

def UsedOnes(dice: List[int]):
    used: List[int] = []
    for d in dice:
        if d == 1:
            used.append(d)
    return used

def UsedFives(dice: List[int]):
    used: List[int] = []
    for d in dice:
        if d == 5:
            used.append(d)
    return used

def UsedAll(dice: List[int]):
    used: List[int] = []
    for d in dice:
        used.append(d)
    return used

def UsedFullHouse(dice: List[int]):
    used: List[int] = []
    dieMap, keys, values = MapDieFaces(dice)
    if IntListIndex(3,values) != -1 and IntListIndex(2,values) != -1:
        for k in keys:
            if dieMap[k] == 2 or dieMap[k] == 3:
                for idx in range(dieMap[k]):
                    used.append(k)
    return used

def UsedStraight(dice: List[int]):
    used: List[int] = []
    _, keys, _ = MapDieFaces(dice)
    keys.sort()
    if ",".join(str(k) for k in keys) == "1,2,3,4,5,6":
        return UsedAll(dice)
    return used

def UsedThreePair(dice: List[int]):
    used: List[int] = []
    _, _, values = MapDieFaces(dice)
    if ",".join(str(v) for v in values) == "2,2,2":
        return UsedAll(dice)
    return used

def UsedDoubleThreeKind(dice: List[int]):
    used: List[int] = []
    _, keys, values = MapDieFaces(dice)
    if ",".join(str(v) for v in values) == "3,3":
        return UsedAll(dice)
    return used

def UsedThreeKind(dice: List[int]):
    used: List[int] = []
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 3:
            for idx in range(dieMap[k]):
                used.append(k)
    return used

def UsedFourKind(dice: List[int]):
    used: List[int] = []
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 4:
            for idx in range(dieMap[k]):
                used.append(k)
    return used

def UsedFiveKind(dice: List[int]):
    used: List[int] = []
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 5:
            for idx in range(dieMap[k]):
                used.append(k)
    return used

def UsedSixKind(dice: List[int]):
    used: List[int] = []
    dieMap, keys, _ = MapDieFaces(dice)
    for k in keys:
        if dieMap[k] == 6:
            return UsedAll(dice)
    return used

def RemoveUsedDice(dice: List[int], used: List[int]):
    remaining: List[int] = []
    for d in dice:
        idx = IntListIndex(d,used)
        if idx == -1:
            remaining.append(d)
        else:
            used.pop(idx)
    return remaining

def TGCategoryScoreAndDice(cat: TenGrandCategory, dice: List[int]):
    score = 0
    used: List[int] = []
    if cat.name == "Ones":
        score = ScoreOnes(dice)
        used = UsedOnes(dice)
    elif cat.name == "Fives":
        score = ScoreFives(dice)
        used = UsedFives(dice)
    elif cat.name == "ThreePairs":
        score = ScoreThreePair(dice)
        used = UsedThreePair(dice)
    elif cat.name == "Straight":
        score = ScoreStraight(dice)
        used = UsedStraight(dice)
    elif cat.name == "FullHouse":
        score = ScoreFullHouse(dice)
        used = UsedFullHouse(dice)
    elif cat.name == "DoubleThreeKind":
        score = ScoreDoubleThreeKind(dice)
        used = UsedDoubleThreeKind(dice)
    elif cat.name == "ThreeKind":
        score = ScoreThreeKind(dice)
        used = UsedThreeKind(dice)
    elif cat.name == "FourKind":
        score = ScoreFourKind(dice)
        used = UsedFourKind(dice)
    elif cat.name == "FiveKind":
        score = ScoreFiveKind(dice)
        used = UsedFiveKind(dice)
    elif cat.name == "SixKind":
        score = ScoreSixKind(dice)
        used = UsedSixKind(dice)
    elif cat.name == "CrapOut":
        used = UsedAll(dice)
    return score, used

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
