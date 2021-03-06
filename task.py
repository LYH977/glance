import datetime
# import time
import os
# import plotly
import redis
from time import sleep
from celery import Celery
import json

from utils.constant import FRAME, TIME, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP, SCATTER_GEO, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE, MAXIMUM, SCATTER_GEO_CONSTANT, MINIMUM
from utils.method import formatted_time_value

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


def extract_max(vtype, obj, max_list, df, parameter, col):
    if vtype ==  SCATTER_MAP:
        for ma in max_list:
            msg = "MAXIMUM '{column}': {field}, by {name} ({lat},{long})".format(
                name=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[NAME]]],
                lat=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LATITUDE]]],
                long=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LONGITUDE]]],
                column=col,
                field=df.loc[ma, col],
            )
            obj[df.loc[ma, FRAME]][MAXIMUM][col].append(msg)
    elif vtype ==  SCATTER_GEO:
        for ma in max_list:
            msg = "MAXIMUM '{column}': {field}, by {name} ({lat},{long})".format(
                name=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[NAME]]],
                lat=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LATITUDE]]],
                long=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LONGITUDE]]],
                column=col,
                field=df.loc[ma, col],
            )
            obj[df.loc[ma, FRAME]][MAXIMUM][col].append(msg)

def extract_min(vtype, obj, min_list, df, parameter, col):
    if vtype ==  SCATTER_MAP:
        for mi in min_list:
            msg = "MININUM for '{column}': {field}, by {name} ({lat},{long})".format(
                name=df.loc[mi, parameter[SCATTER_MAP_CONSTANT[NAME]]],
                lat=df.loc[mi, parameter[SCATTER_MAP_CONSTANT[LATITUDE]]],
                long=df.loc[mi, parameter[SCATTER_MAP_CONSTANT[LONGITUDE]]],
                column=col,
                field=df.loc[mi, col],
            )
            obj[df.loc[mi, FRAME]][MINIMUM][col].append(msg)
    elif vtype ==  SCATTER_GEO:
        for mi in min_list:
            msg = "MININUM '{column}': {field}, by {name} ({lat},{long})".formit(
                name=df.loc[mi, parameter[SCATTER_GEO_CONSTANT[NAME]]],
                lat=df.loc[mi, parameter[SCATTER_GEO_CONSTANT[LATITUDE]]],
                long=df.loc[mi, parameter[SCATTER_GEO_CONSTANT[LONGITUDE]]],
                column=col,
                field=df.loc[mi, col],
            )
            obj[df.loc[mi, FRAME]][MAXIMUM][col].append(msg)


@app.task
def update_data():
    obj = {
        "second": {"third":3}
    }
    # redis_instance.hset(
    #     REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], obj)

    obj = json.dumps(obj)
    print(obj)
    redis_instance.hset(
         REDIS_HASH_NAME, 'new', obj
    )



@app.task
def process_dataset(create_click, dataframe, vtype, parameter):

    tags = []
    obj = {}
    extract = [MAXIMUM, MINIMUM]
    frames = dataframe[FRAME].unique()

    notif_tags = NOTIFICATION_PARAM[vtype][TAG]
    for f in frames:
        obj[f] = {}
        for e in extract:
            obj[f][e] = {}
            for v in NOTIFICATION_PARAM[vtype][FIELD]:
                obj[f][e][parameter[v]] = []
    for t in notif_tags:
        tags.append(parameter[t])
    print('tags', tags)
    if tags:
        tag_df = dataframe[tags]
        tag_df = tag_df.drop_duplicates()  # Lat, Long, Country
        for i in range(len(tag_df.index)):  # row of tagged data frame
            condition = True
            for col in tags:
                condition = condition & (dataframe[col] == tag_df.loc[i, col])
            target_df = dataframe[condition]
            notif_fields = NOTIFICATION_PARAM[vtype][FIELD]
            fields = []
            for f in notif_fields:
                fields.append(parameter[f])
            for col in fields:  # Confirmed, Deaths
                column = target_df[col]
                max_value = column.max()
                min_value = column.min()

                if max_value != min_value:
                    # find max
                    max_list = target_df.index[target_df[col] == max_value].tolist()
                    extract_max(vtype, obj, max_list, target_df, parameter, col)

                    # find min
                    min_list = target_df.index[target_df[col] == min_value].tolist()
                    extract_min(vtype, obj, min_list, target_df, parameter, col)

    print('done obj')
    obj = json.dumps(obj)
    print(obj)
    redis_instance.hset(
         REDIS_HASH_NAME, 'last', obj
    )