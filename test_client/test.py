import asyncio
import datetime
import logging
import json
import websockets
import random

async def data_send(ws):
  await ws.send(json.dumps({
    'msg_name': 'data',
    'sensor_id': 'gresystem000001',
    'transaction_id': '123456789',
    'timestamp': str(datetime.datetime.now()),
    'data': [
      {
        'probe_id': 1,
        'probe_type': 'CT',
        'power': random.sample(range(1000, 3000), 20),
        'pf': random.sample(range(60, 100), 20),
        'voltage': random.randint(212, 228)
        # 'power': [20, 30, 20, 30, 40, 50, 30, 30, 20, 20],
        # 'pf': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        # 'voltage': 220
      },
      {
        'probe_id': 2,
        'probe_type': 'CT',
        'power': random.sample(range(1000, 3000), 20),
        'pf': random.sample(range(60, 100), 20),
        'voltage': random.randint(212, 228)
      },
      {
        'probe_id': 3,
        'probe_type': 'CT',
        'power': random.sample(range(1000, 3000), 20),
        'pf': random.sample(range(60, 100), 20),
        'voltage': random.randint(212, 228)
      }
    ]
  }))
  conf = await ws.recv()
  print('Message received:', conf)

async def main():

  async with websockets.connect(
      'ws://127.0.0.1:5000/powermon/data/gresystem000001'
  ) as ws:

    loop = asyncio.get_running_loop()
    end_time = loop.time() + 20.0
    while True:
        await data_send(ws)
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(main())