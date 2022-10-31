# http post client

import requests, json
from datetime import datetime

URL = 'http://127.0.0.1:5000/powermon/data/'
headers = {'Content-Type': 'application/json; charset=utf-8'}

data = {
  'version': '221017',
  'sensor_id': 'gresystem000001',
  'token': '123456789',
  'timestamp': str(datetime.now()),
  'data': {
    'power': [20, 30, 20, 30, 40, 50, 30, 30, 20, 20],
    'pf': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'voltage': str(220)
  }
}
res = requests.post(URL, headers=headers, data=json.dumps(data))

print(res.content)