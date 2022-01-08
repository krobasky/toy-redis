from redis import Redis
from rq import Queue
from rq.job import  Job

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import stdout_queue_item

for i in range(0,3):
    # Simple example
    job = q.enqueue(stdout_queue_item, i)
    print('Job id (Simply queued) : %s' % job.id)
    # Demonstration: controlled enqueue
    job = q.enqueue(stdout_queue_item,
                    args=(i,),                 # arguments to the job's function (e.g, 'stdout_queue_item')
                    job_id="my_id_" + str(i), # if job_id is missing, unique id is assigned; uniqueness not enforced
                    ttl=(i+1)*60*60,          # timeout after (i+1) hours; default is not timeout
                    kwargs={
                        "description": "Function just prints 'i' to stdout", # passed to stdout_queue_item
                        "ttl": ((i+1)*60.0*60.0/2.0)                          # passed to stdout_queue_item
                    }
                    ) 
    print('Job id (controlled): %s' % job.id)
    # Demonstration: non-unique job ids
    job = q.enqueue(stdout_queue_item, i, job_id="my_id")
    print('Job id (non-unique id): %s' % job.id)

