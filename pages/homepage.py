import datetime
import json

import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objects as go

from app import app
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate

import task
from celery.result import AsyncResult

import base64
import io
import os
import pandas as pd
import redis
import numpy as np
import gif
import cv2
from dash_extensions import Download




# pport = 'redis-12571.c1.ap-southeast-1-1.ec2.cloud.redislabs.com:12571'
# redis_instance = redis.StrictRedis(
#     host=pport,
#     port=12571,
#     password='EGXMBmAkHnhFTLYKGAUEGPdYwf0cZpDC'
# )
from datetime import datetime

# dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
# millisec = dt_obj.timestamp() * 1000
# print(millisec)

# s= 1611918340073422000/  1000000000.0
# dt = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
# print(dt)
from components.visualization import create_figure
from utils.export.export_data import export_mp4
from utils.method import get_ctx_type

print(int(datetime.now().timestamp()) )
redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
N = 100
df = pd.DataFrame(
    {
        "time": [
            i
            for i in range(N)
        ],
        "value": np.random.randn(N),
    }
)
# redis_instance.set( "new", '12' )
# redis_instance.hdel(
#     task.REDIS_HASH_NAME, 'last'
#     )

# task.update_data(df.to_dict())

data = pd.read_csv('C:/Users/FORGE-15/PycharmProjects/glance/datasets/time-series-19-covid-combined.csv')
fig = px.scatter_mapbox(
        data, lat = 'Lat',
        lon = 'Long',
        size = 'Confirmed', size_max = 50,
        color = 'Deaths', color_continuous_scale = px.colors.sequential.Pinkyl,
        hover_name = 'Country/Region',
        mapbox_style = 'dark', zoom=1,
        title='testing',
        animation_frame='Date',
        # animation_group="Province/State",
        # width=swidth ,
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
fig.layout.margin.t = 0
fig.layout.margin.b = 0
fig.layout.margin.r = 0
fig.layout.margin.l = 0
fig.layout.title.pad.t = 0
fig.layout.title.pad.b = 0
fig.layout.title.pad.r = 0
fig.layout.title.pad.l = 0
fig.layout.title.font.color = 'red'
fig.layout.title.y = 0.98
fig.layout.title.x = 0.02
# print((fig.frames))

fig.layout.sliders[0].visible = False
fig.layout.updatemenus[0].visible = False



# fig.layout.coloraxis.colorbar.bgcolor = 'rgba(255,255,255,0.7)'
# fig.layout.coloraxis.colorbar.xanchor = 'right'
# fig.layout.coloraxis.colorbar.xpad = 10
# fig.layout.coloraxis.colorbar.x = 1
# fig.layout.coloraxis.colorbar.title.font.color = 'rgba(255,0,0,1)'
# fig.layout.coloraxis.colorbar.tickfont.color= 'rgba(255,0,0,1)'
# fig.layout.coloraxis.colorbar.len = 1
# fig.layout.coloraxis.colorbar.yanchor = 'bottom'

# fig.layout.coloraxis.colorbar.bordercolor = '#333'


# df = px.data.election()
# df.to_csv('election.csv')


toast = html.Div(
    [
        dbc.Button(
            "Open toast", id="positioned-toast-toggle", color="primary"
        ),
        dbc.Toast(
            "This toast is placed in the top right",
            id="positioned-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            duration=5000,

            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 0, "right": 10, "width": 350, 'background': 'white'},
        ),

    ]
)

layout = dbc.Jumbotron(
    [   toast,
        # html.Span(id='submit-button', n_clicks=0, className='fa fa-send'),

        dcc.Store(id='testing-js', data=fig),
        # dcc.Store(id='testing-plot', data= fig),
        dcc.Graph(id='hp-fig', figure = fig, config={
                    # 'modeBarButtonsToRemove': ['pan2d','select2d', 'lasso2d', 'zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox','toggleHover','toImage'],
                    # 'displaylogo': False,
                    # 'responsive': False,
                    # 'editable': True,
                    'displayModeBar': False
                }),
        html.A('Download test.mp4', id='export-link', download='test.mp4', href='/assets/test.mp4', hidden= True),
        html.Button('export btn', id='export-btn'),
        dcc.Store(id='export-name', data= None),

        dcc.Interval(
                id= 'export-interval',
                interval=1000,
                n_intervals=0,
                disabled=True
            ),

        html.Button('client', id='client-btn'),
        html.P(
            "initial\n1",
            className="lead",
            id='client-p',
            style={"whiteSpace": "pre"}
        ),
        html.Button('test2', id='test2'),
        html.P(
            "avenger assem,ble",
            className="lead",
            id='title2'
        ),
        html.Button('testcelery', id='testcelery'),
        html.H1("Glance", className="display-3"),
        html.P(
            "Watch the world with a glance",
            className="lead",
            id='title'
        ),
        html.Hr(className="my-2"),
        html.P(
            "Jumbotrons use utility classes for typography and "
            "spacing to suit the larger container."
        ),
        html.P(dbc.Button("Learn more", color="primary"), className="lead"),


    ]
)




@app.callback(Output('title', 'children'),
              Input('testcelery', 'n_clicks'))
def update_output(click):
    if click is not None:
        # lala = redis_instance.hset( "new" )
        lala = redis_instance.get('new').decode("utf-8")
        # print('see here:',lala)

        return 'dd'


@app.callback(Output('title2', 'children'),
              Input('test2', 'n_clicks'))
def update_output(click):
    if click is not None:
        # print('clicked test2')
        task.update_data.delay(2)
        return 'spider'






app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='second_function'
    ),
    Output('client-p', 'children'),
    Input('client-btn', 'n_clicks'),
    State('testing-js', 'data'),
    prevent_initial_call=True

)


@gif.frame
def plot(data, datei):
    fig = px.scatter_mapbox(
        data, lat='Lat',
        lon='Long',
        size='Confirmed', size_max=50,
        color='Deaths', color_continuous_scale=px.colors.sequential.Pinkyl,
        hover_name='Country/Region',
        mapbox_style='dark', zoom=1,
        title=datei

    )
    fig.layout.margin.t = 0
    fig.layout.margin.b = 0
    fig.layout.margin.r = 0
    fig.layout.margin.l = 0
    fig.layout.title.pad.t = 0
    fig.layout.title.pad.b = 0
    fig.layout.title.pad.r = 0
    fig.layout.title.pad.l = 0
    fig.layout.title.font.color = 'red'
    fig.layout.title.y = 0.98
    fig.layout.title.x = 0.02
    fig.write_image("yourfile.png")
    return fig


@app.callback(
    Output("positioned-toast", "is_open") ,
    [Input("positioned-toast-toggle", "n_clicks")],
    prevent_initial_call=True
)
def open_toast(n):
    if n:
        return True
    return False



@app.callback(
    [
        Output("export-link", "download"),
        Output("export-link", "href"),
        Output("export-link", "hidden"),
        Output("export-btn", "hidden"),
    ] ,
    [Input("export-btn", "disabled")],
    [State('export-name', 'data'), State('hp-fig', 'figure')],
    prevent_initial_call=True

)
def open_toast(disabled, name, fig):
    if disabled:
        export_mp4(fig, name)
        dl = f'{name}.mp4'
        path = f'/assets/export/{dl}'
        print('habis href')
        return dl, path, False, True
    else:
        return None, None, True, dash.no_update


@app.callback(
    [
        Output("export-btn", "disabled"),
        Output("export-interval", "disabled"),
        Output("export-name", "data"),
    ] ,
    [Input("export-btn", "n_clicks")],
    State("export-btn", "disabled"),
    prevent_initial_call=True
)
def open_toast(btn_click, disabled):
    # print('called')
    #
    # ctx = dash.callback_context
    # if not ctx.triggered:
    #     input_type = 'No input yet'
    # else:
    #     input_type = get_ctx_type(ctx)

    if  btn_click and not disabled :
        now = int(datetime.now().timestamp())
        print('btn part')
        return True, False, now

    raise PreventUpdate







# @app.callback(
#     Output("export-link", "hidden"),
#     [Input("export-btn", "n_clicks"), Input("export-link", "href")],
#     prevent_initial_call=True
# )
# def open_toast( click, href):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         input_type = 'No input yet'
#     else:
#         input_type = get_ctx_type(ctx)
#     if input_type == 'export-btn' and click:
#         return True
#     if input_type == 'export-link' and href:
#         return False
#     raise PreventUpdate



@app.callback(
    Output("export-interval", "n_intervals"),
    [Input("export-link", "n_clicks")],
    prevent_initial_call=True
)
def open_toast( click):
    return 0