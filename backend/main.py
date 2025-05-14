from fastapi import FastAPI
from websocket_chat import router as chat_router
from bot_engine import bot_controller
import asyncio

app = FastAPI()
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_controller())  # Start bots

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
