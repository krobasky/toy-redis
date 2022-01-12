# Redis for Python using Docker, simple example
Useful tools:
* run_worker.py
* create_timeout_job.py <seconds> <job_id>
* get_status.py <job_id>
* stop_job.py <job_id>

## Requirements:
 -  miniconda version 4.11.0+
 -  docker 20.10.11 (for Windows 10+, 16GB RAM+, recommend WSL2 and docker desktop)
 -  docker-compose 3.2 (for Windows/WSL, docker-compose is packaged with docker desktop)
```
conda create -n redis python
conda activate redis
conda install --file requirements.txt
```
## Build container
```
docker-compose up --build -d
```

## Confirm build
```
CONTAINER_ID=`docker ps|grep toy-redis|cut -d ' ' -f 1`
docker exec -it ${CONTAINER_ID} sh
redis-cli
ping
#  PONG
```
^D out of client, ^D out of docker container

## Demonstration

Open 2 terminals (Terminal 1, Terminal 2)

###  create a queue/add jobs
In terminal 1:
```
python use_queue.py
# queue 2 jobs
```
### monitor queue
In terminal 2:
```
rq info -i 1
```
### execute jobs
In terminal 1:
```
python run_worker.py #  alternative: $ rq worker --url redis::/redis:6379
# execute 2 jobs
```
## Clean-up

<br>Terminal 1: ^C out of run_worker
<br>Terminal 2: ^C out of rq

```
docker-compose down
```
confirm:
```
docker network ls
docker ps
```
If toy-redis network remains (e.g., due to `container stop`), remove with:
```
docker network rm `docker network ls|grep toy-redis|cut -d ' ' -f 1`
docker prune
conda deactivate 
# optionally: conda env remove -n redis
```

## Duplicate id demonstration

The scheduler allows the user to provide the job_id, and there's no
unique identifier enforcement. When a new job is enqueued with the
same id as a job already enqueued, the enqueued job's job function and
job function arguments are replaced by the new job's.

### create a queue/add duplicate id jobs
```
python create_duplicate_job_ids.py
# queue 2 jobs with duplicate job id's, but different job functions and job function arguments
```
### execute jobs
```
python run_worker.py 
# executes 2 jobs, both with the last job function and arguments specified
# ^C out of worker
```

## Job status demonstration

```
python use_queue.py
python job_status.py
python run_worker.py
^C
python job_status.py

```
## Timeout demonstration

Job times out after default time of 180s, returns 'failed' status

Open 2 terminals (Terminal 1, Terminal 2)

### create a long job on the queue
In terminal 1:
```
python create_timeout_job.py long_job_id 190
```

### run worker
In terminal 2:
```
python run_worker.py
```

### watch status change to 'failed'
In terminal 1:
```
sh> for i in [[0..100]]; do python get_status.py long_job_id ; sleep 5 ; done
```
## Stopping jobs demonstration

Stopping jobs with status "failed", "finished", or "queued" (not started yet) will throw an exception (InvalidJobOperation). Creating 2 jobs with identical job ids can have unpredictable job ids can have unpredictable results.

Open 2 terminals (Terminal 1, Terminal 2)

### create 2 jobs that will timeout, id='long_job_id'
In terminal 1:
```
python create_timeout_job.py 190 long_job_id
python create_timeout_job.py 190 long_job_id
```
### Issue commands to stop all jobs with id='long_job_id' BEFORE running worker
In terminal 1:
```
python stop_job.py long_job_id
```
Command will fail, throwing exception (InvalidJobOperation) indicating that job is 'queued', not 'started'

### run worker
In terminal 2:
```
python run_worker.py
```

### Issue commands to stop all jobs with id='long_job_id' currently running
In terminal 1:
```
python stop_job.py long_job_id # 1st command
python stop_job.py long_job_id # 2nd command
python stop_job.py long_job_id # 3rd command
```
The following will happen:
 - 1st command: 
   1. Worker will indicate that the first command stops first job with id='long_job_id'.
   2. Worker will start the second job with id='long_job_id'.
 - 2nd command: 
   1. Worker will stop the second job with id='long_job_id'.
 - 3rd command will fail throwing exception (InvalidJobOperation) indicating that job is 'stopped', not 'started'

