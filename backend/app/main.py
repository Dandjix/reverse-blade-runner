from fastapi import FastAPI
from app.api.room_routes import router as room_router
from app.api.game_routes import router as game_router
from app.api.ws_routes import router as ws_router

app = FastAPI()

app.include_router(room_router, prefix="/api", tags=["rooms"])
app.include_router(game_router, prefix="/api", tags=["game"])
app.include_router(ws_router, tags=["websocket"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    
"""

start : 
  cd backend
  python -m app.main 
  
"""