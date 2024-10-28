from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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