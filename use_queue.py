from redis import Redis
from rq import Queue
from rq.job import  Job

redis_connection = Redis()
q = Queue(connection=redis_connection, name="toy_queue")

from queueables import stdout_queue_item_1
# Simple example
hi_str="hello world"
bye_str="hasta luego"
my_id = "my_id"
job = q.enqueue(stdout_queue_item_1, hi_str)
print('+ Job id (Simple enqueue) : %s' % job.id)

# Demonstration: controlled enqueue
job = q.enqueue(stdout_queue_item_1,
                args=(hi_str,),                 # arguments to the job's function (e.g, 'stdout_queue_item_1')
                job_id=my_id,              # if job_id is missing, unique id is assigned; uniqueness not enforced
                ttl=60*60,                      # timeout after an hour; default is not timeout
                kwargs={
                    "description": "Function just prints arg to stdout", # passed to stdout_queue_item_1
                    "ttl": (60.0*60.0/2.0)                          # passed to stdout_queue_item_1
                }
                ) 
print('+ Job id (Controlled enqueue) : %s' % job.id)

from queueables import analyze, post_analyses
#Demonstration: dependent jobs
analysis1_job = q.enqueue(analyze, "normalize")
print('+ [%s] (%s : %s)' % (analysis1_job.get_status(), analysis1_job.func_name, analysis1_job.id, ) )
analysis2_job = q.enqueue(analyze, "PCA", depends_on=analysis1_job)
print('+ [%s] (%s : %s)' % (analysis2_job.get_status(), analysis2_job.func_name, analysis2_job.id ) )
post_job = q.enqueue(post_analyses, "email analysis", depends_on=analysis2_job)
print('+ [%s] (%s : %s)' % (post_job.get_status(), post_job.func_name, post_job.id ) )
