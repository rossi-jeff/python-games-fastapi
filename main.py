from fastapi import FastAPI
from routes import free_cell_route, word_route, concentration_route, klondike_route, poker_square_route, spider_route

app = FastAPI()

app.include_router(concentration_route.router)
app.include_router(free_cell_route.router)
app.include_router(klondike_route.router)
app.include_router(poker_square_route.router)
app.include_router(spider_route.router)
app.include_router(word_route.router)
