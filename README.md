# Simple redis for Python using docker, example

## Requirements:
 -  miniconda version 4.11.0+
 -  docker 20.10.11 (for Windows 10+, 16GB RAM+, recommend WSL2 and docker desktop)
 -  docker-compose 3.2 (for Windows/WSL, docker-compose is packaged with docker desktop)
```
conda create -n redis python
conda activate
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
# queue 3 jobs
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
# execute 3 jobs
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
