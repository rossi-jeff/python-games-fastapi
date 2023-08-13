from typing import List
from sqlalchemy.orm import Session
from models.code_breaker_guess import CodeBreakerGuess

def CalculateGuessKeys(guess: List[str], solution: List[str]):
    white = 0
    black = 0
    for idx in range(len(solution)):
        if guess[idx] == solution[idx]:
            black = black + 1
            guess[idx] = ""
    for color in solution:
        for idx in range(len(guess)):
            if guess[idx] != "" and color == guess[idx]:
                white = white + 1
                guess[idx] = ""
                break
    return black, white

def CalculateCodeBreakerStatus(black: int, columns: int, guesses: int):
    if black == columns:
        return "Won"
    if guesses >= columns * 2:
        return "Lost"
    return "Playing"

def CalculateCodeBreakerScore(db: Session, id: int, columns: int, colors: int):
    perColumn = 10
    perColor = 10
    perBlack = 10
    perWhite = 5
    colorBonus = perColor * colors
    perGuess = perColumn * columns
    maxGuesses = columns * 2
    score = (maxGuesses * perGuess) + colorBonus
    guesses = db.query(CodeBreakerGuess).where(CodeBreakerGuess.code_breaker_id == id).all()
    for guess in guesses:
        score = score - perGuess
        for key in guess.keys:
            if key.Key == 0:
                score = score + perBlack
            elif key.Key == 1:
                score = score + perWhite
    return score