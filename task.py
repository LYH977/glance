import datetime
# import time
import os
# import plotly
import redis
from time import sleep
from celery import Celery

app = Celery("Celery App", broker=os.environ['REDIS_URL'] ,backend=os.environ['REDIS_URL'])
redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])

REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
REDIS_KEYS = {"DATASET": "DATASET", "DATE_UPDATED": "DATE_UPDATED"}

@app.task
def update_data():
    redis_instance.hset(
        REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    )