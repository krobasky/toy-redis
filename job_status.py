from redis import Redis
from rq import Queue
from rq.job import Job

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

# Possible status values are "queued", "started", "deferred", and "finished"
# Possible result values are "None" or not "None"
print("+ Fetching 'my_id' job...")
jobs = Job.fetch_many(['my_id'], connection=redis_connection)
for job in jobs:
    print('+ Status (%s:%s): [%s]' % (job.id, job.func_name, job.get_status()))

print("+ Fetching all jobs...")
queued_job_ids = Job.fetch_many(q.job_ids, connection=redis_connection)
for job in queued_job_ids:
    print('+ Status (%s:%s): [%s]' % (job.id, job.func_name, job.get_status()))

