import sys

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.command import send_stop_job_command

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

job_id = sys.argv[1]

print("+ Fetching job id=(%s)..." % (job_id) )
jobs = Job.fetch_many([job_id], connection=redis_connection)
print("+ Stopping job id=(%s)..." % (job_id) )
for job in jobs:
    print('+ Status (%s:%s): [%s]' % (job.id, job.func_name, job.get_status()))
    try:
        send_stop_job_command(redis_connection, job_id)
    except Exception as e:
        print("! Exception ", e.__class__ , " occurred, message=[", e , "]")
        print('! Status (%s:%s): [%s]' % (job.id, job.func_name, job.get_status()))

