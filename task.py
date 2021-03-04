import datetime
# import time
import os
# import plotly
import redis
from time import sleep
from celery import Celery

from utils.constant import FRAME

app = Celery("Celery App", broker='redis://localhost:6379' ,backend='redis://localhost:6379')
redis_instance = redis.StrictRedis.from_url('redis://localhost:6379')

# pport = 'redis-12571.c1.ap-southeast-1-1.ec2.cloud.redislabs.com:12571'
# redis_instance = redis.StrictRedis(
#     host=pport,
#     port=12571,
#     password='EGXMBmAkHnhFTLYKGAUEGPdYwf0cZpDC'
# )
# app = Celery("Celery App", broker=12571 ,backend=12571)


REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
REDIS_KEYS = {
    "DATASET": "DATASET",
    "DATE_UPDATED": "DATE_UPDATED"
}

@app.task
def update_data():
    redis_instance.hset(
        REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    )



@app.task
def process_dataset(create_click, dataframe, vtype, parameter):
    df_frame = dataframe[FRAME].unique()


    redis_instance.hset(
        REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    )