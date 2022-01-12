from redis import Redis
from rq import Queue
from rq.job import  Job

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import configurable_duration_1

import sys
duration = sys.argv[1]
my_id = sys.argv[2]
long_job = q.enqueue(configurable_duration_1, args=(duration,),  job_id=my_id)
print('+ Job (longer than 180 timeout) - [%s] (%s : %s)' % (long_job.get_status(), long_job.func_name, long_job.id ) )

