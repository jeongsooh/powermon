import asyncio
import datetime
import logging
import json
import websockets
import random
import uuid

async def data_send(ws, count):

  max_count = 100
  if (count // max_count) % 2 == 1:
    power_max = 3000
    power_min = 2500
  else:
    power_max = 1000
    power_min = 800

  message = [2, str(uuid.uuid4()), 'MeterValues', 
    {
      'connectorId': 1, 
      'transactionId': 2265, 
      'meterValue': [
        {
          # 'timestamp': str(datetime.datetime.now()), 
          'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 
          'sampledValue': [
            {
              'probe': 1,
              'probeType': 'CT',
              'power': random.sample(range(power_min, power_max), 20),
              'powerfactor': random.sample(range(60, 100), 20),
              'voltage': random.sample(range(209, 231), 20)
            },
            {
              'probe': 2,
              'probeType': 'CT',
              'power': random.sample(range(power_min, power_max), 20),
              'powerfactor': random.sample(range(60, 100), 20),
              'voltage': random.sample(range(209, 231), 20)
            },
            {
              'probe': 3,
              'probeType': 'CT',
              'power': random.sample(range(power_min, power_max), 20),
              'powerfactor': random.sample(range(60, 100), 20),
              'voltage': random.sample(range(209, 231), 20)
            }
          ]
        }
      ]
    }
  ]
  await ws.send(json.dumps(message))
  conf = await ws.recv()
  print('Echo message # {} received: {}'.format(count, conf))

async def main():

  async with websockets.connect(
      'ws://127.0.0.1:5000/powermon/data/gre000004'
  ) as ws:

    loop = asyncio.get_running_loop()
    end_time = loop.time() + 10.0
    count = 0
    while True:
        await data_send(ws, count)
        count += 1
        # if (loop.time() + 1.0) >= end_time:
        #     break
        await asyncio.sleep(1)

asyncio.run(main())