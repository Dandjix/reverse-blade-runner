from fastapi import FastAPI
from app.api.room_routes import router as room_router
from app.api.game_ws import router as ws_router

app = FastAPI()

app.include_router(room_router, prefix="/api", tags=["rooms"])
app.include_router(ws_router, tags=["websocket"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

#   python -m app.main