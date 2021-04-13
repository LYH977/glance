import tkinter as tk

import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import os

from components.visual.controls import controls_markup
from components.visual.figures.figure_method import create_figure
from components.visual.intervals import intervals_markup
from components.visual.name_section import name_section_markup
from components.visual.setting import setting_markup
from components.visual.stores import stores_markup
from utils import collection
from utils.constant import TIME

from utils.method import get_last_timestamp

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)
# root = tk.Tk()
# swidth = root.winfo_screenwidth()
# data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
# data = pd.read_csv(data_url)
#

def create_visualization(screen_height, screen_width, create_clicks,  param, maxValue, df_frame, tformat,dbname, now, new_col):
    # last_nano = get_last_timestamp(collection.temp[TIME])
    figure = create_figure(collection.data[create_clicks], param['parameter'], param['vtype'])
    # total_rows = len(collection.data[create_clicks].index)
    return html.Div(
        id={'type': 'visualization-container', 'index': create_clicks},
        className='visualization-container',
        style={
            'height': screen_height* 0.72,
            'width': screen_width/2.2,
               },
        children=html.Div([
            stores_markup(create_clicks, param, figure, tformat,  df_frame[0], dbname, now,  new_col),
            intervals_markup(create_clicks, maxValue),

            dbc.Row(
                [
                    dbc.Col( name_section_markup(create_clicks),  width = 'auto'),

                    dbc.Col( setting_markup(create_clicks, param['vtype']), width = 'auto' ),


                ],
                justify="around",
                align= 'center',
            ),
            dcc.Graph(
                # responsive= False,
                className='visualization',
                id={'type': 'visualization', 'index': create_clicks},
                figure = figure,
                config={
                    'modeBarButtonsToRemove': [
                        'pan2d','select2d', 'lasso2d', 'zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox','toggleHover',
                        'zoom2d','zoomIn2d', 'zoomOut2d',  'autoScale2d', 'resetScale2d', 'toggleSpikelines',
                        'hoverClosestCartesian', 'hoverCompareCartesian', 'zoomInGeo', 'zoomOutGeo', 'hoverClosestGeo', 'resetGeo'
                    ],
                    'displaylogo': False,
                    # 'responsive': False,
                    # 'displayModeBar': False
                }
            ),

            html.Div(
                id={'type': 'option-wrapper', 'index': create_clicks},
                className= 'option-wrapper',
                style={ 'height': '15%', },#40% including card body
                children=[
                    controls_markup(create_clicks, maxValue, df_frame[0]),
                    html.Div(
                        id={'type': "loading-notif-output", 'index': create_clicks},
                        children=dbc.Spinner(
                            color="light",
                            type="grow"
                        ),
                    ),
                ]
            ),

        ],className= 'visual-box '
        ),
    )




