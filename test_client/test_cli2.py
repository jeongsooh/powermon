import asyncio
import logging
import json
import websockets

from datetime import datetime

print("Sample code for powermon client")

async def heartbeat_send(ws):
    while True:
      await ws.send(json.dumps({
        'version': '221017',
        'sensor_id': 'gresystem000001',
        'token': '123456789',
        'timestamp': str(datetime.now()),
        'data': {
          'power': [20, 30, 20, 30, 40, 50, 30, 30, 20, 20],
          'pf': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          'voltage': str(220)
        }
      }))
      conf = await ws.recv()
      print('Message received:', conf)
      await asyncio.sleep(10)

async def main():

    async with websockets.connect(
        'ws://127.0.0.1:8000/powermon/data/202021'
    ) as ws:

        await asyncio.gather(
          heartbeat_send(ws),
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
