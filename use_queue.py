from redis import Redis
from rq import Queue, Worker

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import stdout_queue_item

for i in range(0,3):
    job = q.enqueue(stdout_queue_item, i)
    print(str(job))

