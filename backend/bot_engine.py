import asyncio
import websockets
import random
import string
import config.config_manager as config_manager

BOT_NAMES = ["Alex", "Jamie", "Riley", "Sam", "Casey","Johnson","Dick","Volker","Anthony","Mark"]
ACTIVE_BOTS = {}

async def simulate_bot(name: str):
    uri = "ws://localhost:8000/ws/chat"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(name)
            print(f"🤖 {name} connected.")
            while True:
                wait = random.randint(3, 9)
                await asyncio.sleep(wait)
                
                # Ask for context
                from manager import ConnectionManagerInstance
                context = ConnectionManagerInstance.get_context()
                from ai_bot import get_ai_response
                reply = await get_ai_response(context, name)
                
                await websocket.send(reply)
    except Exception as e:
        print(f"Bot {name} error: {e}")

async def bot_controller():
    while True:
        # Add or remove bots randomly
        if len(ACTIVE_BOTS) < 10 and random.random() < 0.9:
            new_bot = random.choice([b for b in BOT_NAMES if b not in ACTIVE_BOTS])
            task = asyncio.create_task(simulate_bot(new_bot))
            ACTIVE_BOTS[new_bot] = task
        elif len(ACTIVE_BOTS) > 0 and random.random() < 0.04:
            to_remove = random.choice(list(ACTIVE_BOTS.keys()))
            ACTIVE_BOTS[to_remove].cancel()
            del ACTIVE_BOTS[to_remove]
            print(f"🤖 {to_remove} left the chat.")
        await asyncio.sleep(15)
