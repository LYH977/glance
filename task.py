import datetime
import time
import os
import plotly
import redis
from time import sleep
from operator import itemgetter

from celery import Celery
import json
import pandas as pd
import numpy as np


from utils.constant import FRAME, TIME, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE, MAXIMUM, MINIMUM, BAR_CHART_RACE, DENSITY, BAR_CHART_RACE_CONSTANT, \
    ITEM, DENSITY_CONSTANT, CHOROPLETH, CHOROPLETH_CONSTANT, LOCATIONS, PERCENT

app = Celery("Celery App", broker='redis://localhost:6379' ,backend='redis://localhost:6379')
redis_instance = redis.StrictRedis.from_url('redis://localhost:6379')



# REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
# REDIS_KEYS = {
#     "DATASET": "DATASET",
#     "DATE_UPDATED": "DATE_UPDATED"
# }

def merge_celery_data(current_frame, next_frame):
    for key in current_frame.keys():
        if key == 'frame':
            continue
        for nested_key in current_frame[key].keys():
            current_frame[key][nested_key] = current_frame[key][nested_key] + next_frame[key][nested_key]


def parse_number(value):
    if value.is_integer():
        return int(value)
    else:
        return float("{:.2f}".format(value))

def extract_extrema(vtype,  ma, df, parameter, col, type):
    msg = ''
    field = 0
    name = ''
    if vtype ==  SCATTER_MAP:
        field = parse_number(df.loc[ma, col])
        name = df.loc[ma, parameter[SCATTER_MAP_CONSTANT[NAME]]]
        msg = "{type} *{column}* : **{field}**, by `{name}({lat},{long})`".format(
            type = type,
            name = name,
            lat = df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LATITUDE]]],
            long = df.loc[ma, parameter[SCATTER_MAP_CONSTANT[LONGITUDE]]],
            column = col,
            field = field
        )

    # elif vtype ==  SCATTER_GEO:
    #     field = parse_number(df.loc[ma, col])
    #     name = df.loc[ma, parameter[SCATTER_GEO_CONSTANT[NAME]]]
    #     msg = "{type} *{column}* : **{field}**, by `{name}({lat},{long})`".format(
    #         type = type,
    #         name = name,
    #         lat = df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LATITUDE]]],
    #         long = df.loc[ma, parameter[SCATTER_GEO_CONSTANT[LONGITUDE]]],
    #         column = col,
    #         field = field,
    #     )
    elif vtype == BAR_CHART_RACE:
        field = parse_number(df.loc[ma, col])
        name = df.loc[ma, parameter[BAR_CHART_RACE_CONSTANT[ITEM]]]
        msg = "{type} *{column}* : **{field}** by `{item}`".format(
            type = type,
            column = col,
            field = field,
            item = name,
        )
    elif vtype == DENSITY:
        field = parse_number(df.loc[ma, col])
        msg = "{type} *{column}* : **{field}**, by `({lat},{long})`".format(
            type = type,
            lat = df.loc[ma, parameter[DENSITY_CONSTANT[LATITUDE]]],
            long = df.loc[ma, parameter[DENSITY_CONSTANT[LONGITUDE]]],
            column = col,
            field = field,
        )

    elif vtype == CHOROPLETH:
        field = parse_number(df.loc[ma, col])
        name = df.loc[ma, parameter[CHOROPLETH_CONSTANT[NAME]]]
        msg = "{type} *{column}* : **{field}**, by `{name}({location})`".format(
            type = type,
            name = name,
            location = df.loc[ma, parameter[CHOROPLETH_CONSTANT[LOCATIONS]]],
            column = col,
            field = field
        )
    return {'msg':msg, 'field':field, 'name':name}

def extract_percent(vtype,  id, df, parameter, col, previous, current):
    msg = ''
    name = ''
    percent = (current-previous) / previous * 100
    movement = '+' if percent >= 0 else '-'  #↑↓
    percent = parse_number(percent)

    if vtype ==  SCATTER_MAP:
        # field = parse_number(df.loc[ma, col])
        name = df.loc[id, parameter[SCATTER_MAP_CONSTANT[NAME]]]

        msg = "**{movement}{field}%** *{column}* : {previous} → {current}, by `{name}({lat},{long})`".format(
            name = name,
            lat = df.loc[id, parameter[SCATTER_MAP_CONSTANT[LATITUDE]]],
            long = df.loc[id, parameter[SCATTER_MAP_CONSTANT[LONGITUDE]]],
            column = col,
            field = abs(percent),
            movement=movement,
            current = current,
            previous = previous
        )

    elif vtype == BAR_CHART_RACE:
        # field = parse_number(df.loc[ma, col])
        name = df.loc[id, parameter[BAR_CHART_RACE_CONSTANT[ITEM]]]
        msg = "**{movement}{field}%** *{column}* : {previous} → {current} by `{item}`".format(
            column = col,
            field = abs(percent),
            item = name,
            movement=movement,
            current=current,
            previous=previous
        )
    elif vtype == DENSITY:
        msg = "**{movement}{field}%** *{column}* : {previous} → {current}, by `({lat},{long})`".format(
            lat = df.loc[id, parameter[DENSITY_CONSTANT[LATITUDE]]],
            long = df.loc[id, parameter[DENSITY_CONSTANT[LONGITUDE]]],
            column = col,
            field = abs(percent),
            movement=movement,
            current=current,
            previous=previous
        )

    elif vtype == CHOROPLETH:
        # field = parse_number(df.loc[ma, col])
        name = df.loc[id, parameter[CHOROPLETH_CONSTANT[NAME]]]
        msg = "**{movement}{field}%** *{column}* : {previous} → {current}, by `{name}({location})`".format(
            name = name,
            location = df.loc[id, parameter[CHOROPLETH_CONSTANT[LOCATIONS]]],
            column = col,
            field = abs(percent),
            movement=movement,
            current=current,
            previous=previous
        )
    return {'msg':msg, 'field':percent, 'name':name}



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
    # sender.add_periodic_task(
    #     15,  # seconds
    #     # an alternative to the @app.task decorator:
    #     # wrap the function in the app.task function
    #     export_data.s(),
    #     name="Export Data",
    # )

@app.task
def process_dataset(create_click, dataframe, vtype, parameter, now, old_celery = {}):
    dataframe = pd.DataFrame.from_dict(dataframe)
    
    tags = []
    obj = {}
    extract = [MAXIMUM, MINIMUM, PERCENT]
    frames = dataframe[FRAME].unique().tolist() # get all the unique frame
    notif_tags = NOTIFICATION_PARAM[vtype][TAG] # get the tags of selected visual type
    for f in range(len(frames)):  # prepare neccessary attribute in obj dict
        obj[f] = {'frame': frames[f]}
        for e in extract:
            obj[f][e] = {'count':0, 'data':'', 'temp':{}}
            for v in NOTIFICATION_PARAM[vtype][FIELD]:
                obj[f][e]['temp'][parameter[v]] = []

    for t in notif_tags:
        tags.append(parameter[t]) # append necessary tags
    tags = list(dict.fromkeys(tags))

    if tags:
        tag_df = dataframe[tags]  # selected columns, e.g. Lat, Long, Country
        tag_df = tag_df.drop_duplicates()  # remove duplicate items
        tag_list = tag_df.index.tolist()
        notif_fields = NOTIFICATION_PARAM[vtype][FIELD] # get the fields of selected visual type
        fields = []
        for f in notif_fields:
            fields.append(parameter[f]) # append necessary fields

        for i in tag_list:  # row of tagged data frame
            condition = True
            for col in tags:
                condition = condition & (dataframe[col] == tag_df.loc[i, col])
            target_df = dataframe[condition]  # sort out dataframe by country
            for col in fields:  # used columns , e.g. Confirmed, Deaths
                #find percent
                column = target_df[col]
                for index in range(1, len(column)):
                    current = parse_number(column.iloc[index])
                    previous = parse_number(column.iloc[index-1])
                    pid = column.index[index]
                    if current != 0 and previous != 0 and current != previous:
                        obj_data = extract_percent(vtype,  pid, target_df, parameter, col, previous, current)
                        frame = target_df.loc[pid, FRAME]
                        index = frames.index(frame)
                        obj[index][PERCENT]['temp'][col].append(obj_data)
                # end of find percent
                max_value = column.max()
                min_value = column.min()
                if max_value != min_value:
                    # find max
                    max_list = target_df.index[target_df[col] == max_value].tolist()
                    for ma in max_list:
                        obj_data = extract_extrema(vtype,  ma, target_df, parameter, col, MAXIMUM)
                        frame = target_df.loc[ma, FRAME]
                        index=frames.index(frame)
                        obj[index][MAXIMUM]['temp'][col].append(obj_data)
                    # end of find max
                    # find min
                    min_list = target_df.index[target_df[col] == min_value].tolist()
                    for mi in min_list:
                        obj_data = extract_extrema(vtype,  mi, target_df, parameter, col, MINIMUM)
                        frame = target_df.loc[mi, FRAME]
                        index = frames.index(frame)
                        obj[index][MINIMUM]['temp'][col].append(obj_data)
                    # end of find min
        for k in obj.keys(): # index
            for e in extract: # MAX, MIN
                for f in fields:
                    target = obj[k][e]['temp'][f]
                    target = sorted(target, key=itemgetter('name'))
                    target = sorted(target, key=itemgetter('field'),reverse = True)
                    for msg in target:
                        obj[k][e]['count'] += 1
                        obj[k][e]['data'] += msg['msg'] +'\n'
                    obj[k][e]['data'] += '\n'+'------------------------------------------------'+'\n'
                obj[k][e].pop('temp', None)

    print('done obj')
    print('create_click', create_click)
    print('now', now)
    # print(obj)

    if len(old_celery) == 0:
        obj = json.dumps(obj, cls=plotly.utils.PlotlyJSONEncoder)
        redis_instance.set( f'{create_click}-{now}', obj, 30)

    else:
        list1 = list(old_celery.values())
        list2 = list(obj.values())
        merged_list = list1 + list2
        sorted_list = sorted(merged_list, key=lambda i: i['frame'])
        unwanted_index = []
        for index in range(0, len(sorted_list)):
            if index >= len(sorted_list) - 1:
                break
            if sorted_list[index]['frame'] == sorted_list[index + 1]['frame']: # perform merging data here
                merge_celery_data(sorted_list[index], sorted_list[index + 1])
                # sorted_list[index]['data'].append(sorted_list[index + 1]['data'][0])
                unwanted_index.insert(0, index + 1)  # prepend
        for index in unwanted_index:
            sorted_list.pop(index)
        results = {i: v for i,v in enumerate(sorted_list)}
        # print('see here', results)
        obj = json.dumps(results, cls=plotly.utils.PlotlyJSONEncoder)
        redis_instance.set(f'{create_click}-{now}', obj, 30)


@app.task
def update_data(test):
    print("----> update_data")
    N = 100
    df = pd.DataFrame( {"time": [datetime.datetime.now() - datetime.timedelta(seconds=i) for i in range(N) ], "value": np.random.randn(N),})
    redis_instance.set( 'new', json.dumps( df.to_dict(), cls=plotly.utils.PlotlyJSONEncoder, )  )



# @app.task
# def export_data(fig):
#     r = random.randint(0,100)
#     images = []
#     frames = []
#     num_frames = len(fig['frames'])
#     for i in range(10):
#         # temp = data.loc[data['Date'] == timeframes[i]]
#         # fig['data'][0] = fig['frames'][i]['data'][0]
#         fig2 = go.Figure(data=fig['frames'][i]['data'][0], layout=fig['layout'])
#         fig2.layout.title.text = fig['frames'][i]['name']
#         img_bytes = fig2.to_image(format="png")
#         print(f'loading img {r}' )
#         images.append(img_bytes)
#
#     for im in images:
#         nparr = np.fromstring(im, np.uint8)
#         frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#         height, width, layers = frame.shape
#         size = (width, height)
#         frames.append(frame)
#
#     pathout = 'assets/export/test.mp4'
#     out = cv2.VideoWriter(pathout, cv2.VideoWriter_fourcc(*'mp4v'), 2, size)
#     for i in range(len(frames)):
#         out.write(frames[i])
#     out.release()
#     print('done export')
