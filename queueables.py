def stdout_queue_item_1(outitem, description=None, ttl=None):
    print( "++ [ {0}:from stdout_queueble_item_1 ]".format(str(outitem)) )

def stdout_queue_item_2(outitem, description=None, ttl=None):
    print( "++ [ {0}:from stdout_queueble_item_2 ]".format(str(outitem)) )

from time import sleep
def configurable_duration_1(job_time:int):
    print( "++ [ job_time={0} ]".format(str(job_time)) )
    sleep(job_time)
    
def analyze(outitem):
    print( "++ [ {0} ]".format(str(outitem)) )
    sleep(5)
    
def post_analyses(outitem, description=None, ttl=None):
    print( "++ [ {0} ]".format(str(outitem)) )
