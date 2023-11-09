import asyncio
import websockets
import json
import uuid
from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from clients.models import Clients
from .consumers import PowermonConsumer

def reset_sensor(sensor_id):
  ocpp_req = {
    "msg_direction" : 2,
    "connection_id" : "",
    "msg_name": "Reset",
    "msg_content": {},
  }
  ocpp_request_to_cp(sensor_id, ocpp_req)

def remotestart_sensor(sensor_id):
  ocpp_req = {
    "msg_direction" : 2,
    "connection_id" : "",
    "msg_name": "RemoteStartTransaction",
    "msg_content": {},
  }
  ocpp_request_to_cp(sensor_id, ocpp_req)

def remotestop_sensor(sensor_id):
  ocpp_req = {
    "msg_direction" : 2,
    "connection_id" : "",
    "msg_name": "RemoteStopTransaction",
    "msg_content": {},
  }
  ocpp_request_to_cp(sensor_id, ocpp_req)

def send_request(sensor_id, message):
  print('OCPP Message : Send to {} : {}'.format(sensor_id, message))
  queryset = Clients.objects.filter(sensor_id=sensor_id).values()
  channel_name = queryset[0]['channel_name']

  channel_layer = get_channel_layer()
  async_to_sync(channel_layer.send)(
    channel_name,
    {
      'type':'ocpp16_message',
      'message': message 
    }
  )

# def connectionid_logging(sensor_id, connection_id, msg_name):
#   queryset = Clients.objects.filter(sensor_id=sensor_id).values()

#   if queryset.count() == 0:
#     client = Clients(
#       sensor_id = sensor_id,
#       connection_id = connection_id,
#       channel_status= msg_name
#     )
#     client.save()
#     print('connection_id saved successfully')
#   else:
#     if not (queryset[0]['connection_id'] == connection_id):
#       Clients.objects.filter(sensor_id=sensor_id).update(connection_id=connection_id, channel_status=msg_name)
#       print('connection_id updated successfully')

def ocpp_request_to_cp(sensor_id, ocpp_req):

  global Job_List 

  ocpp_req['msg_direction'] = 2
  ocpp_req['connection_id'] = str(uuid.uuid4())

  if ocpp_req['msg_name'] == 'Reset':
    ocpp_req['msg_content'] = {
      'type':'Soft',
    }
    message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
    send_request(sensor_id, message)
    # connectionid_logging(sensor_id, ocpp_req['connection_id'], ocpp_req['msg_name'])

  elif ocpp_req['msg_name'] == 'RemoteStartTransaction':
    ocpp_req['msg_content'] = {
      'connectorId':1
    }
    message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
    send_request(sensor_id, message)
    # connectionid_logging(sensor_id, ocpp_req['connection_id'], ocpp_req['msg_name'])

  elif ocpp_req['msg_name'] == 'RemoteStopTransaction':
    queryset = Clients.objects.filter(sensor_id=sensor_id).values()
    transaction_id = queryset[0]['transaction_id']
    ocpp_req['msg_content'] = {
      'transactionId': transaction_id
    }
    message = [ocpp_req['msg_direction'], ocpp_req['connection_id'], ocpp_req['msg_name'], ocpp_req['msg_content']]
    send_request(sensor_id, message)
    # connectionid_logging(sensor_id, ocpp_req['connection_id'], ocpp_req['msg_name'])

  else:
    pass







  