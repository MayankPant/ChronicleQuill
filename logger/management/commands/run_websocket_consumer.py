from django.core.management.base import BaseCommand
import pika
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Run the websocket consumer that sends logs to the frontend'

    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='websocket_queue')

        def callback(ch, method, properties, body):
            log_data = json.loads(body)
            # Send the log data via a Django Channels websocket connection
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'log_group',  # Assuming a group called 'log_group' in Django Channels
                {
                    'type': 'log.message',
                    'message': log_data
                }
            )
            print(f"Sent log to websocket: {log_data}")

        channel.basic_consume(queue='websocket_queue', on_message_callback=callback, auto_ack=True)
        print('WebSocket consumer started. Waiting for messages...')
        channel.start_consuming()
