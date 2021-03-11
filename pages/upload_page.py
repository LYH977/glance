import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from utils import  collection
from utils.method import unpack_parameter
import base64
import io
import pandas as pd
from database.dbConfig import client, new_client



layout = html.Div([
    dcc.Store(id='form-complete', data = False),
    dcc.Upload(
        id='upload-dataset',
        children=html.Button('Upload File'),
        multiple=True
    ),
    html.Div(id = 'preview'),
    dbc.FormGroup(
        [
            dbc.Label("Choose Datetime column*", html_for="dropdown"),
            dcc.Dropdown(
                id="dt-dropdown",
                disabled= True,
            ),
        ]
    ),
    html.Div(id = 'dt-modifier'),
    dbc.Button("Upload", id="dt-upload", className="ml-auto",color="success", disabled=True),
])




def preview_markup(filename):
    return html.Div([
        html.H6(f'Filename: {filename}'),
        html.H6('Below are the first 5 rows.'),
        dash_table.DataTable(
            data=collection.temp.head(5).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in collection.temp.columns]
        ),
    ])



def dt_modifier_markup(value):
    dt = collection.temp.loc[0, value]
    # print(list(collection.temp.columns))
    newCol = list(collection.temp.columns)
    newCol.remove(value)
    options = [{"label": i, "value": i} for i in newCol]
    return dbc.FormGroup(
        [
            dcc.Store(id='dt-filled', data = False),
            dcc.Store(id='dt-format', data= False),
            dbc.Label('Measurement Name*'),
            dbc.Input(id='name-input', placeholder="e.g. Coronavirus", type="text"),
            dbc.FormGroup(
                [
                    dbc.Label("Tags", html_for="dropdown"),
                    dcc.Dropdown(
                        id="dt-tags",
                        multi = True,
                        options = options
                    ),
                ]
            ),
            dbc.Label('Specify datetime format of "{}"'.format(dt)),
            dbc.Input(id='dt-input', placeholder="Input goes here...", type="text"),
            dbc.FormText("20.12.2016 09:38:42,76  ->  %d.%m.%Y %H:%M:%S,%f"),
            dbc.FormText("DAY=%d, MONTH=%m, YEAR=%Y, HOUR=%H, MINUTE=%M, SECOND=%S, MILLISEC=%f"),
            dbc.Button("Check format", id="check-dt-format", className="ml-auto", color="secondary")
        ]
    )