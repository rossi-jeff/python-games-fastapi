from fastapi import FastAPI
from routes import (
    free_cell_route, word_route, concentration_route, klondike_route, 
    poker_square_route, spider_route, code_breaker_route, guess_word_route,
    auth_route, hang_man_route, sea_battle_route, ten_grand_route
)

app = FastAPI()

app.include_router(auth_route.router)
app.include_router(code_breaker_route.router)
app.include_router(concentration_route.router)
app.include_router(free_cell_route.router)
app.include_router(guess_word_route.router)
app.include_router(hang_man_route.router)
app.include_router(klondike_route.router)
app.include_router(poker_square_route.router)
app.include_router(sea_battle_route.router)
app.include_router(spider_route.router)
app.include_router(ten_grand_route.router)
app.include_router(word_route.router)
