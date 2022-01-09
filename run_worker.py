from redis import Redis
from rq import Queue, Worker

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import stdout_queue_item_1, stdout_queue_item_2

# Start a worker with a custom name
worker = Worker([q], connection=redis_connection, name='toy_worker')
worker.work()
