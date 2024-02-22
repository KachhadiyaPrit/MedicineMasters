from channels.generic.websocket import WebsocketConsumer , AsyncWebsocketConsumer
import json
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


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        self.accept()
        self.send(text_data = json.dumps({'status' : 'connected'}))
    
    def receive(self, text_data):
        self.send(text_data = json.dumps({'status' : 'we got you'}))

    def disconnect(self, *args , **kwargs):
        print('disconnect')

    def send_notification(self, event):
        data = json.loads(event.get('value'))
        print(data)
        self.send(text_data=json.dumps({'payload' : data}))
        