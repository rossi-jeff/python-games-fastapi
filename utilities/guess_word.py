from typing import List
from sqlalchemy.orm import Session
from models.guess_word_guess_rating import GuessWordGuessRating
from models.guess_word import GuessWord
from models.guess_word_guess import GuessWordGuess
from models.enums import RatingArray, GameStatus, GameStatusArray
import math


def UpdateGuessWord(db: Session, id: int, status: GameStatus, length: int):
    guesses = db.query(GuessWordGuess).where(
        GuessWordGuess.guess_word_id == id).all()
    perGreen = 10
    perBrown = 5
    perGuess = length * perGreen
    maxGuesses = math.ceil((length * 3) / 2)
    score = perGuess * maxGuesses
    for guess in guesses:
        score = score - perGuess
        for rating in guess.ratings:
            if rating.Rating == 2:
                score = score + perGreen
            elif rating.Rating == 1:
                score = score + perBrown
    db.query(GuessWord).where(GuessWord.id == id).update(
        {"Score": score, "Status": GameStatusArray.index(status.name)})
    db.commit()


def GuessWordStatus(green: int, length: int, guesses: int):
    status = GameStatus.Playing
    if green == length:
        status = GameStatus.Won
    elif guesses > math.ceil((length * 3)/2):
        status = GameStatus.Lost
    return status


def CalculateGuessRatings(db: Session, guess_id: int, Guess: str, Word: str):
    count = 0
    green = []
    brown = []
    guess = list(Guess)
    word = list(Word)
    for idx in range(len(guess)):
        if guess[idx] == word[idx]:
            word[idx] = ""
            green.append(idx)
            count = count + 1
    for i in range(len(guess)):
        if IntListIndex(i, green) == -1:
            for j in range(len(word)):
                if word[j] == guess[i]:
                    word[j] = ""
                    brown.append(i)
    for i in range(len(guess)):
        rating = "Gray"
        if IntListIndex(i, green) != -1:
            rating = "Green"
        elif IntListIndex(i, brown) != -1:
            rating = "Brown"
        gwgr = GuessWordGuessRating(
            guess_word_guess_id=guess_id,
            Rating=RatingArray.index(rating)
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
        if len(brown[idx]) > 0 and ListContains(letter, brown[idx]):
            return True
    return False


def MatchGray(word: str, gray: List[str], green: List[str]):
    if len(gray) == 0:
        return False
    allGray = []
    for letter in gray:
        if not ListContains(letter, green):
            allGray.append(letter)
    for letter in word:
        if ListContains(letter, allGray):
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
            if not ListContains(letter, allBrown):
                allBrown.append(letter)
    for letter in allBrown:
        if not ListContains(letter, word):
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
