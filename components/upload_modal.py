import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from utils.constant import FIGURE_OPTION, FIGURE_PARAM, CREATE_BTN_ID, SM_PARAM, SG_PARAM, D_PARAM, CA_PARAM, CH_PARAM, \
    BC_PARAM, SCATTER_MAP, SCATTER_GEO, DENSITY, CHOROPLETH, CAROUSEL, BAR_CHART_RACE
from utils import  collection
from utils.method import unpack_parameter
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
                    html.Div(id='after-upload'),
                    # html.Div(id='data-snapshot'),
                    # html.Div(id='output-form'),
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
            is_open=False,
            autoFocus=False,

        ),
    ]
)

def after_upload_markup(filename):
    return html.Div([
        html.Div(id='data-snapshot',children=snapshot_markup(filename)),
        html.Div(id='output-form'),
    ])





def snapshot_markup (filename):
    return html.Div([
        html.H6(f'Filename: {filename}'),
        html.H6('Below are the first 5 rows.'),
        dash_table.DataTable(
            data=collection.temp.head(5).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in collection.temp.columns]
        ),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Visualization type", html_for="dropdown"),
                dcc.Dropdown(
                    id="visual-type",
                    options=[{"label": i, "value": i} for i in FIGURE_OPTION],
                ),
            ]
        ),
    ])




def output_form_markup(type):
    parameter={}
    for p_id, p_info in FIGURE_PARAM[type].items():
        print(p_id)
        parameter[p_id] = p_info['value']
    return html.Div([
        # dcc.Store(id='uuid', data=None),
        dcc.Store(id='parameter', data = parameter),
        # dcc.Store(id='is-filled', data = False),
        # dcc.Store(id=CREATE_BTN_ID[type], data={'filled': False, 'parameter': parameter}),
        dcc.Store(id=SM_PARAM, data={'is_filled': False, 'parameter': parameter if type == SCATTER_MAP else None}),
        dcc.Store(id=SG_PARAM, data={'is_filled': False, 'parameter': parameter if type == SCATTER_GEO else None}),
        dcc.Store(id=D_PARAM, data={'is_filled': False, 'parameter': parameter if type == DENSITY else None}),
        dcc.Store(id=CH_PARAM, data={'is_filled': False, 'parameter': parameter if type == CHOROPLETH else None}),
        dcc.Store(id=CA_PARAM, data={'is_filled': False, 'parameter': parameter if type == CAROUSEL else None}),
        dcc.Store(id=BC_PARAM, data={'is_filled': False, 'parameter': parameter if type == BAR_CHART_RACE else None}),

        dbc.Form(
            [
                parameter_option(i, j, k) for i,j,k in unpack_parameter(FIGURE_PARAM[type])
            ],
            inline=True,
            # style={'background':'red'}
        )
    ])




def parameter_option(name, id, multi = False):
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label(name, className="mr-2"),
                        dcc.Dropdown(
                            style={'width': '100%'},
                            id=id,
                            options=[{"label": i, "value": i} for i in collection.temp.columns],
                            multi = multi
                        ),
                    ],
                    # className="mr-3",
                    style={'width': '50%'}
        )