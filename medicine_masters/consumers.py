from re import A
from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer
import json
from yaml import Event
from .models import *
from asgiref.sync import async_to_sync , sync_to_async


class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_tracking_id']
        self.room_group_name = 'order_%s' % self.room_name
        print('Connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

        order = Order.giver_order_details(self.room_name)

        self.send(text_data=json.dumps({
            'payload' : order
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def recieve(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'order_status',
                'payload' : text_data
            }
        )

    def order_status(self, event):
        order = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload' : order
        }))        


class NewConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'new_consumer'
        self.room_group_name = 'new_consumer_group'

        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({'status' : 'Connect to django project'}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect')

    def recieve(self, text_data):
        print(text_data)
        self.send(text_data=json.dump({'status' : 'we got you'}))

    def send_notification(self, event):
        data = json.loads(event.get('value'))
        print(data)
        self.send(text_data=json.dumps({'payload' : data}))