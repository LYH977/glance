import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app
from dash.dependencies import Input, Output, State

import task
from celery.result import AsyncResult

import base64
import datetime
import io
import os
import pandas as pd
import redis
import datetime


# pport = 'redis-12571.c1.ap-southeast-1-1.ec2.cloud.redislabs.com:12571'
# redis_instance = redis.StrictRedis(
#     host=pport,
#     port=12571,
#     password='EGXMBmAkHnhFTLYKGAUEGPdYwf0cZpDC'
# )
from datetime import datetime

# dt_obj = datetime.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
# # dt_obj = datetime.strptime('2016', '%Y')
# millisec = dt_obj.timestamp() * 1000
# print(millisec)

# s= 1611918340073422000/  1000000000.0
# dt = datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
# print(dt)

redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
task.update_data()
layout = dbc.Jumbotron(
    [
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
        # dcc.Upload(
        #     id='upload-data',
        #     children=html.Button('Upload File'),
        #     multiple=True
        # ),
        # html.Div(id='output-data-upload'),

    ]
)


# def parse_contents(contents, filename, date):
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])
#
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),
#
#         dash_table.DataTable(
#             data=df.head(10).to_dict('records'),
#             columns=[{'name': i, 'id': i} for i in df.columns]
#         ),
#
#         html.Hr(),  # horizontal line
#
#         # For debugging, display the raw contents provided by the web browser
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])
#
#
# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload-data', 'contents'),
#               State('upload-data', 'filename'),
#               State('upload-data', 'last_modified'))
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children


@app.callback(Output('title', 'children'),
              Input('testcelery', 'n_clicks'))
def update_output(click):
    if click is not None:
        lala = redis_instance.hget(task.REDIS_HASH_NAME, task.REDIS_KEYS["DATE_UPDATED"] ).decode("utf-8")
        print(lala)
        return 'dd'