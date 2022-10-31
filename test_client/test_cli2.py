# websockets client (Async)

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
      conf = await ws.recv()
      print('Message received:', conf)
      await asyncio.sleep(interval)

async def main():
    interval = 5
    async with websockets.connect(
        'ws://127.0.0.1:5000/powermon/data/gresystem000001'
    ) as ws:

        await asyncio.gather(
          # interval = sensor_boot(ws),
          data_send(ws, interval),
        )

if __name__ == '__main__':
    try:
        # asyncio.run() is used when running this example with Python 3.7 and
        # higher.
        asyncio.run(main())
    except AttributeError:
        # For Python 3.6 a bit more code is required to run the main() task on
        # an event loop.
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.close()
