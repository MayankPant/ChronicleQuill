
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from .utils import CONSUMER_TOGGLE_NAME, LOG_DB_NAME
from .LogMemory import retrieve_all, set_key, get_key
from . import utils
LEVEL: str = 'debug'
LINES: str = 'all'
SERVICE: str = 'all'

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
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if(data['event'] == 'CONSUMER_TOGGLE'):
            set_key(CONSUMER_TOGGLE_NAME, data['value'])
            print(f'\n\n\n\n\n\nCONSUMER_TOGGLE: {get_key(CONSUMER_TOGGLE_NAME)}')

    
     # Handler for messages received from the channel layer
    async def logging_message(self, event):
        # Send message to WebSocket
        print(f'Triggered message handler: {event}')
        await self.send(text_data=json.dumps(event))


class ServiceLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # join a group when connecting
        self.room_group_name = 'service_logger'
        self.keep_sending_logs = True
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
        
    async def receive(self, text_data=None, bytes_data=None):
        print(f'Received message from frontend: {text_data}')
        data = json.loads(text_data)
        if data['event'] == 'FILTER':
            global LEVEL, LINES, SERVICE
            LEVEL = data['level']
            LINES = data['lines']
            SERVICE = data['service']
            print(f'Global variables Level: {LEVEL}, lines: {LINES}, service: {SERVICE}')
        
        if(data['event'] == 'CONSUMER_TOGGLE'):
            set_key(CONSUMER_TOGGLE_NAME, data['value'])
            print(f'\n\n\n\n\n\nCONSUMER_TOGGLE: {get_key(CONSUMER_TOGGLE_NAME)}')
    
    # sends service specific logs to the frontend
    async def send_log_batches(self, event):
        print(f"Entered the send log batches: ")
        logs = self.get_latest_logs(batch_size=event['batch_size'])
        if logs and len(logs) > 0:
            await self.send(text_data=json.dumps(logs))
            
    
    def get_latest_logs(self, batch_size: int) -> dict:
        logs = retrieve_all(LOG_DB_NAME)
        filtered_logs = filter(self.filter_logs, logs)
        filtered_logs = [log  for log in filtered_logs]
        return filtered_logs
        
    def filter_logs(self, log: str):
        log_data = json.loads(log)
        if LEVEL == 'all':
            return log_data['service'] == SERVICE
        return log_data['service'] == SERVICE and  log_data['level'].lower() == LEVEL