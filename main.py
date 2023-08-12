from fastapi import FastAPI
from routes import free_cell_route, word_route, concentration_route

app = FastAPI()

app.include_router(concentration_route.router)
app.include_router(free_cell_route.router)
app.include_router(word_route.router)
