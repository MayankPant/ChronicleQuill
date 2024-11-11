from django.core.management.base import BaseCommand
import pika
import json
from ...utils import LOG_DB_NAME, send_logs, send_batches, CONSUMER_TOGGLE_NAME
import environ
from ...LogMemory import insert, get_key

env = environ.Env(
    DEBUG=(bool, False)
)

credentials = pika.PlainCredentials(env('RABBITMQ_DEFAULT_USER'), env('RABBITMQ_DEFAULT_PASS'))

"""

The following command send the logging message to the chronicle quill
client. The UI interface provides a much better way of interacting
with the logs
"""

class Command(BaseCommand):
    help = 'Run the websocket consumer that sends logs to the frontend'

    def handle(self, *args, **kwargs):
        print(f'Entered the websocket consumer handler')
        # hearbeat defines how long the channel stays open after staying idle and no data transfer
        connection = pika.BlockingConnection(pika.ConnectionParameters(heartbeat=600, host='rabbitmq', credentials=credentials))
        channel = connection.channel()

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        
         # just in case the exchange is not declared
        channel.exchange_declare(exchange='logs_exchange', exchange_type='fanout')
        channel.queue_bind(exchange='logs_exchange', queue=queue_name)

        def callback(ch, method, properties, body):
            log_data = json.loads(body)
            print(f"\n\n\n\nRecieved Log Data from message broker: {log_data}\n CONSUMER_TOGGLE: {get_key(CONSUMER_TOGGLE_NAME)}")
            # Send the log data via a Django Channels websocket connection
            if get_key(CONSUMER_TOGGLE_NAME) in [1, '1']: # no idea whats the return type so two values
                insert(body, LOG_DB_NAME)
                send_batches()
            else:
                send_logs(json.dumps(log_data), log_data['service'])
            ch.basic_ack(delivery_tag = method.delivery_tag)
            print(f"Sent log to websocket: {log_data}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        print('WebSocket consumer started. Waiting for messages...')
        channel.start_consuming()
