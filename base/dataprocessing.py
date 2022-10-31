from datetime import datetime

def power_data_processing(message):
  conf = {
    'msg_name': message['msg_name'],
    'sensor_id': message['sensor_id'],
    'transaction_id': message['transaction_id'],
    'timestamp': str(datetime.now())
  }
  return conf