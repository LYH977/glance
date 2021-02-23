import json
from utils.constant import FIGURE_PARAM

def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
        value = dataframe[i] if i % 7 == 0 else ''
        calendar.append(value)
    return calendar


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
