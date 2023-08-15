from typing import List
from sqlalchemy.orm import Session
from payloads.sea_battle_payload import SeaBattlePoint
from models.sea_battle_ship import SeaBattleShip
from models.sea_battle_turn import SeaBattleTurn
import random

MaxAxisH = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
MaxAxisV = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
Directions = ["N","S","E","W"]

def EmptyGrid(axis: int):
    grid = {}
    for idxH in range(axis):
        grid[MaxAxisH[idxH]] = {}
        for idxV in range(axis):
            grid[MaxAxisH[idxH]][MaxAxisV[idxV]] = False
    return grid

def OpponentFirePoint(db: Session, id: int, axis: int):
    point: SeaBattlePoint | None = None
    grid = EmptyGrid(axis)
    turns = db.query(SeaBattleTurn).where(SeaBattleTurn.sea_battle_id == id and SeaBattleTurn.Navy == 1).all()
    for turn in turns:
        grid[turn.Horizontal][turn.Vertical] = True
    found = False
    while not found:
        idxH = random.randint(0,axis-1)
        idxV = random.randint(0,axis-1)
        if not grid[MaxAxisH[idxH]][MaxAxisV[idxV]]:
            point = SeaBattlePoint(
                Horizontal = MaxAxisH[idxH],
                Vertical = MaxAxisV[idxV]
            )
            found = True
    return point

def OpponentShipPoints(db: Session, id: int, axis: int, size: int):
    points: List[SeaBattlePoint] = []
    grid = EmptyGrid(axis)
    ships = db.query(SeaBattleShip).where(SeaBattleShip.sea_battle_id == id and SeaBattleShip.Navy == 1).all()
    for ship in ships:
        for p in ship.points:
            grid[p.Horizontal][p.Vertical] = True
    while len(points) < size:
        points = []
        counter = 0
        idxH = random.randint(0,axis-1)
        idxV = random.randint(0,axis-1)
        direction = random.choice(Directions)
        while counter < size:
            if idxH < 0 or idxH >= axis or idxV < 0 or idxV >= axis:
                break
            Horizontal = MaxAxisH[idxH]
            Vertical = MaxAxisV[idxV]
            if grid[MaxAxisH[idxH]][MaxAxisV[idxV]]:
                break
            points.append({ "Horizontal": Horizontal, "Vertical": Vertical})
            counter = counter + 1
            if direction == "N":
                idxV = idxV - 1
            elif direction == "S":
                idxV = idxV + 1
            elif direction == "E":
                idxH = idxH + 1
            else:
                idxH = idxH - 1
    return points