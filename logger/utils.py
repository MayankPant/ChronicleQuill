from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


LOG_DB_NAME: str = 'logdb'
"""
Log DB name is the name of our shared redis list.
"""
CONSUMER_TOGGLE_NAME: str = 'consumer_toggle'
"""
CONSUMER_TOGGLE is used to toggle the service specific consumer in the run_websocket_consumer
management command.
"""
    
        


def send_logs(message: str, service_name: str):
    
    """
    sends a message to all the connected webssocket clients
    
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'logger',
        {
            'type': 'logging_message',
            'message' : message,
            'service_name': service_name
        }
    )
    print(f'Sent logs to message hanlder')
    
def send_batches(batch_size=10):
    
    """
    sends a batch of logs to the frontend
    
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'service_logger',
        {
            'type': 'send_log_batches',
            'batch_size': batch_size
        }
    )
    print(f'Sent logs to service message hanlder')