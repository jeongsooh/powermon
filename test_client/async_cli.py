#!/usr/bin/env python

import asyncio
import websockets
import time

async def getback(websocket):
  message = await websocket.recv()
  # await asyncio.sleep(3)
  time.sleep(2)
  return message

async def hello():
    async with websockets.connect("ws://127.0.0.1:5000") as websocket:
      count = 0
      while count < 10:
        await websocket.send("Hello world!")
        message = await getback(websocket)
        print(message)
        count += 1

asyncio.run(hello())