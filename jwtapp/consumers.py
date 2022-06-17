import json
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_room"
        self.room_group_name = "test_room_group"
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.send(text_data=json.dumps({"status": "connected from django channels"}))

    def receive(self, text_data):
        self.send(text_data=json.dumps({"status": "way to go receiver"}))

    def disconnect(self, close_code):
        print("channels is disconnected")

    def send_notification(self, event):
        self.send(text_data=json.dumps(event.get("value")))
        
class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = "new_test_room"
        self.room_group_name = "new_test_room_group"
        await(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"status": "connected from new consumer"}))
    

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"status": "way to go receiver"}))
        
    async def disconnect(self, close_code):
        print("channels is disconnected")

    async def send_new_notification(self, event):
        print(event)
        await self.send(text_data=json.dumps(event.get("value")))
