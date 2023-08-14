from typing import List

def MatchGreen(word: str, green: List[str]):
    if NoGreen(green):
        return True
    for idx in range(len(word)):
        if word[idx] != green[idx] and green[idx] != "":
            return False
    return True

def MatchBrown(word: str, brown: List[List[str]]):
    if len(brown) == 0:
        return False
    for idx in range(len(word)):
        letter = word[idx]
        if len(brown[idx]) > 0 and ListContains(letter,brown[idx]):
            return True
    return False

def MatchGray(word: str, gray: List[str], green: List[str]):
    if len(gray) == 0:
        return False
    allGray = []
    for letter in gray:
        if not ListContains(letter,green):
            allGray.append(letter)
    for letter in word:
        if ListContains(letter,allGray):
            return True
    return False

def NoGreen(green: List[str]):
    for letter in green:
        if letter != "":
            return False
    return True

def IncludeAllBrown(word: str, brown: List[List[str]]):
    allBrown = []
    for idx in range(len(word)):
        for letter in brown[idx]:
            if not ListContains(letter,allBrown):
                allBrown.append(letter)
    for letter in allBrown:
        if not ListContains(letter,word):
            return False
    return True

def ListContains(token: str, argList: List[str]):
    for letter in argList:
        if letter == token:
            return True
    return False