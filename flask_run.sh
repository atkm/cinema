#!/bin/bash
redis-server&
REDIS_PID=$!
python -m cinema.worker&
WORKER_PID=$!
flask run

# kill background processes on SIGINT
trap "kill $REDIS_PID; kill $WORKER_PID" INT
