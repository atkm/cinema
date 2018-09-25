import os
import redis
from rq import Worker, Queue, Connection

listen = ['default']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_conn = redis.from_url(redis_url)

# TODO: preload libraries (models, keyword_extraction_db) to avoid the import overhead of each worker. Ref: Performance notes section in rq docs.

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
