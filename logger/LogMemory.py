import redis

redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

"""
    Initially in order to store logs I thought of simply creating a
    dequeue instance and store the logs in it. Then later import the instance somewhere
    else and use the stored data. Unfortunately that dosent work.
    
    Since management commands run as seperate processes the memeory for
    objects is not shared. Hence we need to create a shared memory space for
    our websocket consumer to share resources with our main
    django application.
    
    For this we use redis dataabase for fast writing and reading and shared
    memory space.
"""


def test_connection():
        """
        Tests the connection
        """
        try:
            redis_client.ping()
            print("Connected to Redis!")
            return "SUCESS"
        except redis.ConnectionError:
            print("Unable to connect to Redis.")
            return 'FAILURE'
    
def insert(text_data: str, dequeue_name: str):
    """
    Inserts the data at the tail end of a dequeue
    """
    redis_client.rpush(dequeue_name, text_data)

def retrieve(dequeue_name: str):
    return redis_client.lpop(dequeue_name)

def retrieve_all(dequeue_name: str, batch_size: int = None):
    data =  redis_client.lrange(dequeue_name, 0, -1)
    redis_client.ltrim(dequeue_name, 1, 0)
    return data

def get_length(dequeue_name: str) -> int:
    return redis_client.llen(dequeue_name)
    
    
        
