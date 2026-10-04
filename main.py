from app.api.v1.snakes import router as snakes_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(snakes_router)
