import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from trello_clone_api.routers.boards import router as board_router
from trello_clone_api.routers.cards import router as card_router

app = FastAPI()

app.include_router(board_router)
app.include_router(card_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    # asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
