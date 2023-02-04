# websockets client (Sync)

import asyncio
import json
import websockets

from datetime import datetime

print("Sample code for powermon client")

async def print_response(response):
    print(response)

async def data_send(ws, interval):

    # send a message to the server
    message = json.dumps({
      'msg_name': 'data',
      'sensor_id': 'gresystem000001',
      'transaction_id': '123456789',
      'timestamp': str(datetime.now()),
      'data': {
        'probe_id': 1,
        'probe_type': 'CT',
        'power': [20, 30, 20, 30, 40, 50, 30, 30, 20, 20],
        'pf': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'voltage': 220
      }
    })
    await ws.send(message)
    while True:
      # wait for a response from the server
      response = await ws.recv()
      asyncio.create_task(print_response(response))

      # await asyncio.sleep(interval)
      await asyncio.sleep(interval)
      await ws.send(message)

async def main():
  async with websockets.connect(
      'ws://127.0.0.1:5000/powermon/data/gre000003'
  ) as ws:

    await data_send(ws, interval=10)

if __name__ == '__main__':
  asyncio.run(main())
  
