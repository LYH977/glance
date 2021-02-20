import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from utils.constant import FIGURE_TYPE, SCATTER_MAP_PARAM
import base64
import io
import pandas as pd

modal = html.Div(
    [
        # dbc.Button("Select File", id="open"),
        html.Div('add',id="open", style={'width':200, 'height':200, 'background':'red'}),
        dbc.Modal(
            [
                dbc.ModalHeader("Create New Visualization"),
                dbc.ModalBody(html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Button('Upload File'),
                        multiple=True
                    ),
                    html.Div(id='temp'),
                    html.Div(id='output-data-upload'),
                ])),
                dbc.ModalFooter(
                    html.Div([
                        dbc.Button("Create", id="create", className="ml-auto",color="success", disabled=True),
                        dbc.Button("Close", id="close", className="ml-auto",color="danger"),
                    ])
                ),
            ],
            id="modal",
            size="xl",
            backdrop='static',

        ),
    ]
)
