from redis import Redis
from rq import Queue
from rq.job import  Job

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import stdout_queue_item_1, stdout_queue_item_2
# Simple example
hi_str="hello world"
bye_str="hasta luego"

# Notably, enqueuing with a non-unique job_id will not replace currently enqueued jobs of the same job_id
#   but it will replace the job function and arguments of currently enqueued jobs of the same job_id
print("+ -- Demonstration: multiple identical job id's create multiple identical jobs on the queue, with new job functions replacing enqueue'd job functions")
job = q.enqueue(stdout_queue_item_1, hi_str, job_id="my_id")
print('+ Non-unique id status(hi_str,%s:%s): [%s]' % (job.id,job.func_name, job.get_status() ))
job = q.enqueue(stdout_queue_item_2, bye_str, job_id="my_id")
print('+ Non-unique id status(bye_str,%s:%s):[%s]' % (job.id,job.func_name, job.get_status()))
print('+ Running the worker will print the bye_str from function _2 twice, once per duplicate id')

