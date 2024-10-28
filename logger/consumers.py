from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # join a group when connecting
        self.room_group_name = 'logger'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f'Websocket connection successfull')
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f'Websocket disconnection successfull')

    
     # Handler for messages received from the channel layer
    async def logging_message(self, event):
        # Send message to WebSocket
        print(f'triggered message handler: {event}')
        await self.send(text_data=json.dumps(event))