import json
from datetime import datetime
from database.dbConfig import client
import pandas as pd

from utils import collection
from utils.constant import FIGURE_PARAM, STANDARD_T_FORMAT

def reset_var():
    collection.data = {}
    collection.img_container = {}
    collection.visual_container = []
    collection.temp = None

def select_query (measurement,  where=''):
    q = "select * from " + measurement + where
    result = client.query(q, epoch='ns')
    return pd.DataFrame(result[measurement])


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
    props_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if props_id[0] =='{':
        temp = json.loads(props_id)
        obj = temp['type']
    else:
        obj = props_id
    return obj


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
        # print('p_id',p_id)
        # print('p_info',p_info)

        label.append(p_info['label'])
        id.append(p_id)
        multi.append(p_info['multi'])
    # print('label',label)
    # print('id', id)
    # print('multi',multi)

    return zip(label, id, multi)

