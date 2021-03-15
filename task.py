import datetime
import time
import os
import plotly
import redis
from time import sleep
from celery import Celery
import json
import pandas as pd
import numpy as np


from utils.constant import FRAME, TIME, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP, SCATTER_GEO, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE, MAXIMUM, SCATTER_GEO_CONSTANT, MINIMUM, BAR_CHART_RACE, DENSITY, BAR_CHART_RACE_CONSTANT, \
    ITEM, DENSITY_CONSTANT, CHOROPLETH, CHOROPLETH_CONSTANT, LOCATIONS

app = Celery("Celery App", broker='redis://localhost:6379' ,backend='redis://localhost:6379')
redis_instance = redis.StrictRedis.from_url('redis://localhost:6379')
# redis_instance = redis.StrictRedis(db=0)

# pport = 'redis-12571.c1.ap-southeast-1-1.ec2.cloud.redislabs.com:12571'
# redis_instance = redis.StrictRedis(
#     host=pport,
#     port=12571,
#     password='EGXMBmAkHnhFTLYKGAUEGPdYwf0cZpDC'
# )
# app = Celery("Celery App", broker=12571 ,backend=12571)


REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
# print(REDIS_HASH_NAME)
REDIS_KEYS = {
    "DATASET": "DATASET",
    "DATE_UPDATED": "DATE_UPDATED"
}

def parse_number(value):
    # print(type(value))
    if value.is_integer():
        return int(value)

def extract_extrema(vtype,  ma, df, parameter, col, type):
    msg=''
    if vtype ==  SCATTER_MAP:
        msg = "{type} '{column}': {field}, by {name} ({lat},{long})".format(
            type = type,
            name=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[NAME]]],
            lat=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LATITUDE]]],
            long=df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LONGITUDE]]],
            column=col,
            field=parse_number(df.loc[ma, col]),
        )
    elif vtype ==  SCATTER_GEO:
        msg = "{type} '{column}': {field}, by {name} ({lat},{long})".format(
            type=type,
            name=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[NAME]]],
            lat=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LATITUDE]]],
            long=df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LONGITUDE]]],
            column=col,
            field=parse_number(df.loc[ma, col]),
        )
    elif vtype == BAR_CHART_RACE:
        msg = "{type} '{column}': {field} by {item}".format(
            type=type,
            column=col,
            field=parse_number(df.loc[ma, col]),
            item=df.loc[ma, parameter[BAR_CHART_RACE_CONSTANT[ITEM]]],
        )
    elif vtype == DENSITY:
        msg = "{type} '{column}': {field}, by ({lat},{long})".format(
            type=type,
            lat=df.loc[ma, parameter[DENSITY_CONSTANT[LATITUDE]]],
            long=df.loc[ma, parameter[DENSITY_CONSTANT[LONGITUDE]]],
            column=col,
            field=parse_number(df.loc[ma, col]),
        )

    elif vtype == CHOROPLETH:
        msg = "{type} '{column}': {field}, by {name}({location})".format(
            type=type,
            name=df.loc[ma, parameter[CHOROPLETH_CONSTANT[NAME]]],
            location=df.loc[ma, parameter[CHOROPLETH_CONSTANT[LOCATIONS]]],
            column=col,
            field=parse_number(df.loc[ma, col]),
        )
    return msg





@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        15,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        update_data.s(),
        name="Update data",
    )
    sender.add_periodic_task(
        15,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        process_dataset.s(),
        name="Process Dataset",
    )

@app.task
def process_dataset(create_click, dataframe, vtype, parameter):
    dataframe = pd.DataFrame.from_dict(dataframe)
    print('starting')
    tags = []
    obj = {}
    extract = [MAXIMUM, MINIMUM]
    frames = dataframe[FRAME].unique().tolist()
    # print(frames)
    # print(frames.index('2020-01-22'))
    notif_tags = NOTIFICATION_PARAM[vtype][TAG]
    # for t in range(len(frames)):
    #     print(frames[t])

    for f in range(len(frames)):
        obj[f] = {'frame': frames[f]}
        for e in extract:
            obj[f][e] = {'count':0, 'data':'', 'temp':{}}
            for v in NOTIFICATION_PARAM[vtype][FIELD]:
                obj[f][e]['temp'][parameter[v]] = []

    # for f in frames:
    #     obj[f] = {}
    #     for e in extract:
    #         obj[f][e] = {}
    #         for v in NOTIFICATION_PARAM[vtype][FIELD]:
    #             obj[f][e][parameter[v]] = []
    for t in notif_tags:
        tags.append(parameter[t])
    print('tags', tags)
    if tags:
        tag_df = dataframe[tags]
        tag_df = tag_df.drop_duplicates()  # Lat, Long, Country
        # print('tag_df', tag_df)
        tag_list = tag_df.index.tolist()

        notif_fields = NOTIFICATION_PARAM[vtype][FIELD]
        fields = []
        for f in notif_fields:
            fields.append(parameter[f])

        for i in tag_list:  # row of tagged data frame
            condition = True
            for col in tags:
                condition = condition & (dataframe[col] == tag_df.loc[i, col])
            target_df = dataframe[condition]

            for col in fields:  # Confirmed, Deaths
                column = target_df[col]
                max_value = column.max()
                min_value = column.min()

                if max_value != min_value:
                    # find max
                    max_list = target_df.index[target_df[col] == max_value].tolist()
                    for ma in max_list:
                        msg = extract_extrema(vtype,  ma, target_df, parameter, col, MAXIMUM)
                        frame = target_df.loc[ma, FRAME]
                        index=frames.index(frame)
                        obj[index][MAXIMUM]['temp'][col].append(msg)


                    # find min
                    min_list = target_df.index[target_df[col] == min_value].tolist()
                    for mi in min_list:
                        msg = extract_extrema(vtype,  mi, target_df, parameter, col, MINIMUM)
                        frame = target_df.loc[mi, FRAME]
                        index = frames.index(frame)
                        obj[index][MINIMUM]['temp'][col].append(msg)
    # print(obj)
        for k in obj.keys(): # index
            for e in extract: # MAX, MIN
                for f in fields:
                    print('k', k)
                    print('e', e)

                    print('f', f)
                    for msg in obj[k][e]['temp'][f]:
                        obj[k][e]['count'] += 1
                        obj[k][e]['data'] += msg + '\n'
                obj[k][e].pop('temp', None)

    print('done obj')
    obj = json.dumps(obj, cls=plotly.utils.PlotlyJSONEncoder)
    print(obj)
    # redis_instance.hset(REDIS_HASH_NAME, 'new', obj  )
    redis_instance.set( 'new', obj  )

    #
    # @app.task
    # def update_data():
    #     print("----> update_data")
    #     # Create a dataframe with sample data
    #     # In practice, this function might be making calls to databases,
    #     # performing computations, etc
    #     N = 100
    #     df = pd.DataFrame(
    #         {
    #             "time": [
    #                 datetime.datetime.now() - datetime.timedelta(seconds=i)
    #                 for i in range(N)
    #             ],
    #             "value": np.random.randn(N),
    #         }
    #     )
    #
    #     # Save the dataframe in redis so that the Dash app, running on a separate
    #     # process, can read it
    #     redis_instance.hset(
    #         REDIS_HASH_NAME,
    #         REDIS_KEYS["DATASET"],
    #         json.dumps(
    #             df.to_dict(),
    #             # This JSON Encoder will handle things like numpy arrays
    #             # and datetimes
    #             cls=plotly.utils.PlotlyJSONEncoder,
    #         ),
    #     )
    #     # Save the timestamp that the dataframe was updated
    #     redis_instance.hset(
    #         REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    #     )


@app.task
def update_data(test):
    print("----> update_data")
    N = 100
    df = pd.DataFrame(
        {
            "time": [
                datetime.datetime.now() - datetime.timedelta(seconds=i)
                for i in range(N)
            ],
            "value": np.random.randn(N),
        }
    )


    # redis_instance.hset(
    #     REDIS_HASH_NAME,
    #     # REDIS_KEYS["DATASET"],
    #     'last',
    #     json.dumps(
    #         df.to_dict(),
    #         cls=plotly.utils.PlotlyJSONEncoder,
    #     ),
    # )
    redis_instance.set( 'new', json.dumps(
            df.to_dict(),
            cls=plotly.utils.PlotlyJSONEncoder,
        )  )
    # redis_instance.set('new', '100')
    # redis_instance.hset(
    #     REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    # )