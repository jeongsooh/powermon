import asyncio
import logging
import json
import websockets

from datetime import datetime

print("Sample code for powermon client")

def heartbeat_send(ws):
    while True:
      ws.send(json.dumps({
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
      conf = ws.recv()
      print('Message received:', conf)
      sleep(10)

def main():

  with websockets.connect(
      'ws://127.0.0.1:8000/powermon/data/202022'
  ) as ws:

    heartbeat_send(ws),

if __name__ == '__main__':

  main()
