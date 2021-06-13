import copy
import json
from datetime import datetime
from database.dbConfig import client
import pandas as pd
import numexpr as ne

from utils import collection
from utils.constant import FIGURE_PARAM, STANDARD_T_FORMAT, FRAME

def store_template(param1, param2 = {}):
    return {
        0:param1,
        2:param2
    }


def reset_marker_trace():
    return {
        'lat': [],
        'lon': [],
        'marker': {'size': 0},
        'mode': 'markers',
        'showlegend': False,
        'type': 'scattermapbox'
    }


def insert_marker (name, coordinate):
    if name == 'unknown':
        formatted_name = coordinate + '<extra></extra>'
    else:
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
    # print('coo', coordinate)
    return {
        # 'coloraxis': "coloraxis",
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
        'name': name,
        'customdata':[coordinate],
        'subplot': 'mapbox',
        'type': 'scattermapbox'
    }

def update_legend_theme(legend, fig):
    if legend:  # dark theme
        fig['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,1)'
        fig['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
        fig['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
        # fig['layout']['paper_bgcolor'] = '#000'
        if 'coloraxis2' in fig['layout']:
            fig['layout']['coloraxis2']['colorbar']['bgcolor'] = 'rgba(0,0,0,1)'
            fig['layout']['coloraxis2']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
            fig['layout']['coloraxis2']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'

    else:  # light theme
        fig['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,1)'
        fig['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
        fig['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
        # fig['layout']['paper_bgcolor'] = '#fff'
        if 'coloraxis2' in fig['layout']:
            fig['layout']['coloraxis2']['colorbar']['bgcolor'] = 'rgba(255,255,255,1)'
            fig['layout']['coloraxis2']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
            fig['layout']['coloraxis2']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
    return fig


def update_mapbox_type(mapbox, fig):
    fig['layout']['mapbox']['style'] = mapbox
    return fig


def update_colorscale(colorscale, secondary, fig):
    fig['layout']['coloraxis']['colorscale'] = colorscale['0']['value']
    if len(secondary) != 0 and 'coloraxis2' in fig['layout'] and len(colorscale['2']) != 0:
        fig['layout']['coloraxis2']['colorscale'] = colorscale['2']['value']
    return fig

def update_marker_data(marker, fig):
    fig['data'][1] = marker
    return fig

def update_live_visual_style(fig, legend, mapbox, colorscale, secondary, marker):
    fig = update_legend_theme(legend, fig)
    fig = update_mapbox_type(mapbox, fig)
    if None not in colorscale['0']['value'] :
        print('yes')
        fig = update_colorscale(colorscale, secondary, fig)
    fig = update_marker_data(marker, fig)
    return fig

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
        return pd.DataFrame(result[measurement])
    else:
        return None


def to_nanosecond_epoch(dt):
    return (dt - datetime(1970,1,1)).total_seconds() * pow(10,9)

def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
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

# l = [{'prop_id': '{"index":2,"type":"secondary-visual-btn"}.n_clicks_timestamp', 'value': 1621005270133}, {'prop_id': '{"index":3,"type":"secondary-visual-btn"}.n_clicks_timestamp', 'value': 1621005297733}]




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

def index_frame(frames, num):
   new_frames = []
   for i,fr in enumerate(frames):
       new_fr = copy.deepcopy(fr)
       new_fr['data'][0]['oriIndex'] = f"['frames{num}'][{i}]['data'][0]"
       new_frames.append(new_fr)
   return new_frames



def merge_frames(list1, list2):
    new_list1 = index_frame(list1, 0)
    new_list2 = index_frame(list2, 2)
    pointers_fr = []
    merged_list = new_list1 + new_list2
    sorted_list = sorted(merged_list, key = lambda i: i['name'])
    unwanted_index = []
    for index in range(0, len(sorted_list)):
        if index >= len(sorted_list) -1:
            break
        if sorted_list[index]['name'] == sorted_list[index+1]['name']:
            sorted_list[index]['data'].append(sorted_list[index+1]['data'][0])
            unwanted_index.insert(0, index+1) # prepend

    for index in unwanted_index:
        sorted_list.pop(index)

    for li in sorted_list:
        pointers = []
        for d in li['data']:
            pointers.append(d['oriIndex'])
        pointers_fr.append({
            'name':li['name'],
            'pointers': pointers
        })
    # print(pointers_fr)


    return {
        'frames': pointers_fr,
        'frames0': list1,
        'frames2': list2
    }


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"