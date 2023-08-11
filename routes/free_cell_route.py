from fastapi import APIRouter

router = APIRouter(
    prefix="/api/free_cell",
    tags=["Free Cell"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def free_cells_paginated(Limit = 10, Offset = 0):
    return {"message": "TODO"}

@router.get("/{free_cell_id}")
async def get_free_cell_by_id(free_cell_id: int):
    return {"message": "TODO"}

@router.post("/")
async def create_free_cell():
    return {"message": "TODO"}

@router.patch("/{free_cell_id}")
async def update_free_cell(free_cell_id: int):
    return {"message": "TODO"}