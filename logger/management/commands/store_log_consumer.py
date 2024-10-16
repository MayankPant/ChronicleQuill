from django.core.management.base import BaseCommand
import pika
import json
from ...models import Log
from django.utils import timezone
import environ
"""
This file collects the log messages from a rabbit mq 
message broker. The queues are temporary queues which are going to 
be available as long as the consumers are alive.

"""
env = environ.Env(
    DEBUG=(bool, False)
)

credentials = pika.PlainCredentials(env('RABBITMQ_DEFAULT_USER'), env('RABBITMQ_DEFAULT_PASS'))


class Command(BaseCommand):
    help = 'Run the storage consumer that saves logs to the database'
    
    
    def handle(self, *args, **kwargs):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.18.0.3', credentials=credentials))
        channel = connection.channel()
        # Declare the fanout exchange and bind to a queue

        result = channel.queue_declare(queue='', exclusive=True) # auto delete queue when consumer not in use
        queue_name = result.method.queue
        channel.queue_bind(exchange='logs_exchange', queue=queue_name)
        
        def callback(ch, method, properties, body):
            log_message = json.loads(body)
            print(f"The log message received: {log_message}")
            Log.objects.create(
                level=log_message["level"],
                message=log_message["message"],
                timestamp=log_message.get("timestamp", timezone.now()),
                service_name=log_message.get("service", "AUTH_EVENT"),
            )
            # sending out a basic acknowledgement if the consumer completes its process
            ch.basic_ack(delivery_tag = method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        print(' [*] Waiting for logs to store in DB. To exit press CTRL+C')
        channel.start_consuming()    
    
