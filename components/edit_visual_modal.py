import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from database.dbConfig import client
from utils.constant import FIGURE_OPTION, FIGURE_PARAM, CREATE_BTN_ID, SM_PARAM, SG_PARAM, D_PARAM, CA_PARAM, CH_PARAM, \
    BC_PARAM, SCATTER_MAP, DENSITY, CHOROPLETH, CAROUSEL, BAR_CHART_RACE, TIME_FORMAT, YEAR, SECONDARY_FIGURE_OPTION
from utils import  collection
from utils.method import unpack_parameter
import base64
import io
import pandas as pd

modal = html.Div(
    [

        dcc.Store(id='param-to-edit', data={}),
        # dcc.Store(id='chosen-tformat', data= YEAR),
        # dcc.Store(id='chosen-dropdown', data= None),
        dbc.Modal(
            [
                dbc.ModalHeader("Edit Visualization", id = 'edit-modal-head'),
                dbc.ModalBody(
                    html.Div(id='edit-visual-portal'),
                ),
                dbc.ModalFooter(
                    html.Div([
                        dbc.Button(
                            "Edit",
                            id="edit-visual",
                            className="ml-auto",
                            color="success",
                            disabled=True,
                            # style={'display':'block'}
                        ),
                        dbc.Button("Close", id="cancel-edit-visual", className="ml-auto",color="danger"),
                    ], className= 'mod-footer')
                ),
            ],
            id="edit-visual-modal",
            size="xl",
            backdrop='static',
            is_open=False,
            autoFocus=False,
            # style={'background': 'red'}
            contentClassName='select-modal-content'

        ),
    ],
)

def parameter_option(name, id, value, columns, multi = False):
    if not multi:
        dropdown = dbc.Select(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            value = value
        )
    else:
        dropdown = dcc.Dropdown(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            multi= multi,
            value=value
        )
    return  \
        dbc.FormGroup(
            [
                dbc.Label(name, className="mr-2"),
                dropdown,
            ],
            style={'width': '50%', 'padding':'5px'}
        )


def time_format_option():
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label('Choose Time Format', className="mr-2"),
                        dbc.Select(
                            style={'width': '100%'},
                            id='time-format',
                            options=[{"label": i, "value": j} for i, j in
                                     zip(TIME_FORMAT.keys(), TIME_FORMAT.values())],
                            value=YEAR
                        )
                    ],
                    style={'width': '50%', 'padding':'5px'}
        )

def edit_visual_portal_markup(vtype):
