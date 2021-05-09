import json
from datetime import datetime
from database.dbConfig import client
import pandas as pd
import numexpr as ne

from utils import collection
from utils.constant import FIGURE_PARAM, STANDARD_T_FORMAT, FRAME

def reset_trace():
    return {
        'lat': [],
        'lon': [],
        'marker': {'size': 0},
        'mode': 'markers',
        'showlegend': False,
        'type': 'scattermapbox'
    }


def insert_marker (name, coordinate):
    split_name = name.split(', ')
    formatted_name=''
    for s, i in zip(split_name, range(0, len(split_name))):
        formatted_name += s
        if i != len(split_name)-1:
            formatted_name += ',<br>'
    formatted_name += '<extra></extra>'
    split_coordinate = coordinate.split(', ')
    lat = float(split_coordinate[0][1:])
    long = float(split_coordinate[1][:-1])

    return {
        'coloraxis': "coloraxis",
        'hovertemplate': formatted_name,
        'lat': [lat],
        'lon': [long],
        'marker': {
            'size': 20,
            'symbol': ['embassy'],
            'allowoverlap': True
        },
        'mode': 'markers',
        'showlegend': False,
        # 'legendgroup': '',
        'name': name,
        'coordinate':coordinate,
        'subplot': 'mapbox',
        'type': 'scattermapbox'
    }

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def reset_var():
    collection.data = {}
    collection.img_container = {}
    # collection.visual_container = []
    collection.temp = None

def remove_from_collection(index):
    collection.data.pop(index, None)
    collection.img_container.pop(index, None)
    collection.live_processing.pop(index, None)
    # collection.visual_container = []

def get_last_timestamp(param):
    last_time = param.iloc[-1]
    temp = datetime.strptime(last_time, STANDARD_T_FORMAT)
    return to_nanosecond_epoch(temp)

def select_query (measurement,  where=''):
    q = f'select * from "{measurement}" {where}'
    result = client.query(q, epoch='ns')
    if measurement in result:
        # print(result)
        # test = pd.DataFrame(result[measurement])
        # eq = "- Magnitude"
        # test['Latitude'] = pd.to_numeric(test["Latitude"])
        # see = test.eval(eq)
        # print(see)
        return pd.DataFrame(result[measurement])
    else:
        return None


def to_nanosecond_epoch(dt):
    return (dt - datetime(1970,1,1)).total_seconds() * pow(10,9)

def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
        # value = formatted_time_value(dataframe[i], tformat) if i % 7 == 0 else ''
        value = dataframe[i] if i % 7 == 0 else ''
        calendar.append(value)
    return calendar

def formatted_time_value(time, tformat):
    return datetime.strptime(time, STANDARD_T_FORMAT).strftime(tformat)

def get_ctx_type(ctx):
    obj = ctx.triggered[0]['prop_id'].split('.')[0]
    if obj[0] =='{':
        temp = json.loads(obj)
        type = temp['type']
    else:
        type = obj
    return type


def get_ctx_index(ctx):
    obj = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    return obj['index']


def get_ctx_property(ctx):
    return ctx.triggered[0]['prop_id'].split('.')[1]


def get_ctx_value(ctx):
    return ctx.triggered[0]['value']

def unpack_parameter(param):
    label  =[]
    id  =[]
    multi  =[]
    for p_id, p_info in param.items():

        label.append(p_info['label'])
        id.append(p_id)
        multi.append(p_info['multi'])


    return zip(label, id, multi)

