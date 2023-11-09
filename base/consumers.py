# https://www.youtube.com/watch?v=cw8-KFVXpTE&t=2s

import json
import asyncio
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from clients.models import Clients
from .models import Item
from .dataprocessing import power_data_processing

def channel_logging(sensor_id, channel_name, channel_status, flag):
  queryset = Clients.objects.filter(sensor_id=sensor_id).values()
  if flag == 'REG':
    if queryset.count() == 0:
      client = Clients(
        sensor_id = sensor_id,
        channel_name = channel_name,
        channel_status=channel_status,
      )
      client.save()
      print('channel is saved successfully')
    else:
      if not (queryset[0]['channel_name'] == channel_name):
        Clients.objects.filter(sensor_id=sensor_id).update(channel_name=channel_name, channel_status=channel_status)
        print('channel is updated successfully')
  elif flag == 'DEL':
    if queryset.count() !=0:
      if queryset[0]['channel_status'] == channel_status:
        Clients.objects.filter(sensor_id=sensor_id).delete()
        print('channel is removed successfully')
  else:
    pass

class PowermonConsumer(WebsocketConsumer):

  def connect(self):

    self.room_group_name = 'all_clients'
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name
    )
    channel_logging(channel_name=self.channel_name, sensor_id=self.scope['path_remaining'], channel_status=self.scope['client'], flag='REG')
    self.accept() 

  def disconnect(self, close_code):
    # print(self.scope, dir(self.scope))
    channel_logging(channel_name=self.channel_name, sensor_id=self.scope['path_remaining'], channel_status=self.scope['client'], flag='DEL')

  def receive(self, text_data):
    data = json.loads(text_data)
    sensor_id = self.scope['path_remaining']
    transaction_id = ''

    # print("raw data received", data)

    if data:
      if data[0] == 2:
        if data[2] != "MeterValues":
          print("Power Data : Received from {} : {}".format(sensor_id, data))

          Item.objects.create(
            msg_direction = data[0],
            transaction_id = data[1],
            msg_name = data[2],
            data = data[3],
            sensor_id = sensor_id
          )
        else:
          print("Power Data : Received from {} : {}".format(sensor_id, data))
          transaction_id = data[1]
        conf = power_data_processing(data, sensor_id)
        if conf[1] != transaction_id:
          print("Power Data : Confirmed to {} : {}".format(sensor_id, conf))
          Item.objects.create(
            msg_direction = conf[0],
            transaction_id = conf[1],
            data = conf[2],
          )
        self.send(text_data=json.dumps(conf))
      elif data[0] == 3:
        print("Power Data : Confirmed from {} : {}".format(sensor_id, data))
        Item.objects.create(
          msg_direction = data[0],
          transaction_id = data[1],
          data = data[2],
        )
      else:
        pass
    else:
      conf = [4,'',{}]
      print("Power Data : NO DATA Error Confirmed to {} : {}".format(sensor_id, conf))
      self.send(text_data=json.dumps(conf))

  def ocpp16_message(self, event):
    message = event['message']

    self.send(text_data=json.dumps(message))

  def send(self, text_data=None, bytes_data=None, close=False):
    """
    Sends a reply back down the WebSocket
    """
    if text_data is not None:
        super().send(text_data=text_data)
    elif bytes_data is not None:
        super().send({"type": "websocket.send", "bytes": bytes_data})
    else:
        raise ValueError("You must pass one of bytes_data or text_data")
    if close:
        self.close(close)

