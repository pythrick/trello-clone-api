import asyncio

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from trello_clone_api.db.base import init_models
from trello_clone_api.routers.projects import router as project_router
from trello_clone_api.routers.tasks import router as task_router

app = FastAPI()

app.include_router(project_router)
app.include_router(task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    asyncio.run(init_models())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
