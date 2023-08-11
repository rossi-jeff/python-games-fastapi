from fastapi import FastAPI
from routes import free_cell_route

app = FastAPI()

app.include_router(free_cell_route.router)