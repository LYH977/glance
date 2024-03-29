import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import os

from components.visual.container.visual_box import visual_box_markup
from components.visual.container.visual_mask import visual_mask_markup
from components.visual.figures.figure_method import create_figure
from utils import collection

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)



def create_visualization(screen_height, screen_width, create_clicks,  param, maxValue, df_frame, tformat,dbname, now, new_col):
    figure = create_figure(collection.data[create_clicks], param['parameter'], param['vtype'])
    # print('screen_height',screen_height)
    # print('screen_width',screen_width)

    return html.Div(

        id={'type': 'visualization-container', 'index': create_clicks},
        className='visualization-container',
        style={
                # 'height': screen_height * 0.72,
                # 'width': screen_width / 2.2,
                # 'height': '80vh',
                # 'width': '50vw',
            },
        children=html.Div([
            visual_mask_markup(create_clicks),
            visual_box_markup(create_clicks, param, figure, tformat, df_frame[0], dbname, now, new_col, maxValue),

        ], style={'position':'relative', 'height':'100%', 'width':'100%'}   ),
            )


    # )




