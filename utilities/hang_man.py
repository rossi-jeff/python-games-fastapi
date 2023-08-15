from typing import List
from .guess_word import ListContains
from sqlalchemy.orm import Session

def CalculateHangManStatus(Word: List[str], Correct: List[str], Wrong: List[str]):
    word = StringListUnique(Word)
    correct = StringListUnique(Correct)
    wrong = StringListUnique(Wrong)
    if AllIncluded(word,correct):
        return "Won"
    if len(wrong) >= 6:
        return "Lost"
    return "Playing"

def CalculateHangManScore(Word: List[str], Correct: List[str], Wrong: List[str], status: str):
    score = 0
    word = StringListUnique(Word)
    correct = StringListUnique(Correct)
    wrong = StringListUnique(Wrong)
    perLetter = 10
    perCorrect = 5
    if status == "Won":
        score = len(word) * perLetter
    score = score + (len(correct) * perCorrect)
    score = score - (len(wrong) * perLetter)
    return score

def StringListUnique(strList: List[str]):
    unique = []
    for token in strList:
        if not ListContains(token,unique) and token != "" and token != ",":
            unique.append(token)
    return unique

def AllIncluded(Word: List[str], Correct: List[str]):
    missed = []
    for letter in Word:
        if not ListContains(letter,Correct):
            missed.append(letter)
    return len(missed) == 0
