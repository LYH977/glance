import datetime
import json

import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
from dash.dependencies import Input, Output, State, ClientsideFunction

import task
from celery.result import AsyncResult

import base64
import io
import os
import pandas as pd
import redis
import numpy as np


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
layout = dbc.Jumbotron(
    [
        html.Button('client', id='client-btn'),
        html.P(
            "client",
            className="lead",
            id='client-p'
        ),
        html.Button('stark', id='test2'),
        html.P(
            "avenger assem,ble",
            className="lead",
            id='title2'
        ),
        html.Button('tony', id='testcelery'),
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
        # lala = redis_instance.get( "new" )
        lala = redis_instance.get('new').decode("utf-8")
        print('see here:',lala)

        return 'dd'


@app.callback(Output('title2', 'children'),
              Input('test2', 'n_clicks'))
def update_output(click):

    if click is not None:
        print('clicked test2')

        task.update_data.delay(2)

        return 'spider'


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='second_function'
    ),
    Output('client-p', 'children'),
    Input('client-btn', 'n_clicks'),
)