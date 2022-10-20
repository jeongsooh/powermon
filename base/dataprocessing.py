from datetime import datetime

def power_data_processing(message):
  conf = {
    'sensor_id': message['sensor_id'],
    'token': message['token'],
    'timestamp': str(datetime.now())
  }
  return conf