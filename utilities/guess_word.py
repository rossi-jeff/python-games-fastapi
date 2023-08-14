from typing import List
from sqlalchemy.orm import Session
from models.guess_word_guess_rating import GuessWordGuessRating
from models.enums import RatingArray

def CalculateGuessRatings(db: Session, guess_id: int, Guess: str, Word: str):
    count = 0
    green = []
    brown = []
    guess = list(Guess)
    word = list(Word)
    for idx in range(len(guess)):
        if guess[idx] == word[idx]:
            word[idx] = ""
            green.append(i)
            count = count + 1
    for i in range(len(guess)):
        if IntListIndex(i,green) == -1:
            for j in range(len(word)):
                if word[j] == guess[i]:
                    word[j] = ""
                    brown.append(i)
    for i in range(len(guess)):
        rating = "Gray"
        if IntListIndex(i,green) != -1:
            rating = "Green"
        elif IntListIndex(i,brown) != -1:
            rating = "Brown"
        gwgr = GuessWordGuessRating(
            guess_word_guess_id = guess_id,
            Rating = RatingArray.index(rating)
        )
        db.add(gwgr)
        db.commit()
    return count

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

def IntListIndex(token: int, intList: List[int]):
    for idx in range(len(intList)):
        if intList[idx] == token:
            return idx
    return -1