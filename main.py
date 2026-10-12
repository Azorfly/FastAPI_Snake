from app.api.v1.snakes import router as snakes_router
from app.exceptions import SnakeNotFound
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
app = FastAPI()

app.include_router(snakes_router)

@app.exception_handler(SnakeNotFound)
async def snake_not_found_handler(request: Request, exc: SnakeNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})