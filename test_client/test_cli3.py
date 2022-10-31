# websockets client (Sync)

import asyncio
import logging
import json
import websockets

from datetime import datetime

print("Sample code for powermon client")

async def data_send(ws, interval):
    while True:
      await ws.send(json.dumps({
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
      }))
      await ws.recv()
      async for message in ws:
        print('Message received:', message)
      await asyncio.sleep(interval)

async def main():
  async with websockets.connect(
      'ws://127.0.0.1:5000/powermon/data/gresystem000002'
  ) as ws:

    await data_send(ws, interval=10)

if __name__ == '__main__':
  asyncio.run(main())
  
