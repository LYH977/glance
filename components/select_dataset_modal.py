import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from database.dbConfig import client
from utils.constant import FIGURE_OPTION, FIGURE_PARAM, CREATE_BTN_ID, SM_PARAM, SG_PARAM, D_PARAM, CA_PARAM, CH_PARAM, \
    BC_PARAM, SCATTER_MAP, SCATTER_GEO, DENSITY, CHOROPLETH, CAROUSEL, BAR_CHART_RACE, TIME_FORMAT, YEAR
from utils import  collection
from utils.method import unpack_parameter
import base64
import io
import pandas as pd



modal = html.Div(
    [
        # dbc.Button("Select File", id="open"),
        html.Button(
            # html.P('+',className='add_btn' ),
            html.I(className="fa fa-plus fa-lg"),
            id="open",
            className='floating_area'
        ),
        dcc.Store(id='last-param', data={}),
        dcc.Store(id='chosen-tformat', data= YEAR),

        dcc.Store(id='chosen-dropdown', data= None),
        dbc.Modal(
            [
                dbc.ModalHeader("Create New Visualization"),
                dbc.ModalBody(html.Div([
                    html.Div(id='dataset-window'),
                    html.Div(id='dataset-portal'),
                ])),
                dbc.ModalFooter(
                    html.Div([
                        dbc.Button("Create", id="create-visual", className="ml-auto",color="success", disabled=True),
                        dbc.Button("Close", id="cancel-create-visual", className="ml-auto",color="danger"),
                    ])
                ),
            ],
            id="modal",
            size="xl",
            backdrop='static',
            is_open=False,
            autoFocus=False,

        ),
    ],
    # style={    'position':'relative', 'width':'inherit', 'height':'inherit'}
)

def dataset_portal_markup(filename):
    return html.Div([

        html.Div(id='data-snapshot',children=snapshot_markup(filename)),
        html.Div(id='output-form'),
    ])



def snapshot_markup (filename):
    return html.Div([
        html.Div([
            html.H6(f'Filename: {filename}'),
            html.H6('Below are the first 5 rows.'),
            dash_table.DataTable(
                id = 'portal-datatable',
                data = collection.temp.head(5).to_dict('records'),
                columns = [{'name': i, 'id': i} for i in collection.temp.columns],

            ),
            html.Div([
                dbc.Button(
                    "Open collapse",
                    id="click-target",
                    className="mb-3",
                    color="primary",
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader(
                            [
                                dcc.Input(
                                    id='new-column-name',
                                    type="text",
                                    maxLength=10,
                                    size='13',
                                    placeholder='Column Name'
                                ),
                                '= ',
                                html.P('(Equation will appear here)', className='equation-window',
                                         id='equation-window'),

                            ],
                            # style={'width':'500px'}
                        ),
                        dbc.PopoverBody(
                            [
                                dcc.Store(id=f'operand-type', data={ 0:'dropdown', 1:'dropdown', 2:'dropdown' }),
                                html.Div([    expression_box_markup(n) for n in range(0,3)  ], className='expression-wrapper' ),
                                # html.Div( 'Equation will appear here', className = 'equation-window', id = 'equation-window' ),
                                html.Div([
                                    dbc.Button( "Confirm", id="confirm-new-col", className="mb-3", color="primary" , disabled= True),
                                    dbc.Button( "Reset", id="reset-new-col", className="mb-3", color="danger"  ),
                                ]),

                            ],
                            # style={'maxWidth': '500px'}
                        ),
                    ],
                    id="click",
                    target="click-target",
                    trigger="click",
                    # style={'maxWidth':'500px'}
                ),
            ]),
        ]
        , style={'overflow':'auto'}),

        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Visualization type", html_for="dropdown"),
                dbc.Select(
                    id="visual-type",
                    options=[{"label": i, "value": i} for i in FIGURE_OPTION],
                )
            ]
        ),
    ])




def output_form_markup(type):
    parameter={}
    for p_id, p_info in FIGURE_PARAM[type].items():
        parameter[p_id] = p_info['value']
    options = [ parameter_option(i, j, k) for i,j,k in unpack_parameter(FIGURE_PARAM[type]) ]
    options.append(time_format_option())
    return html.Div([
        dcc.Store(id=SM_PARAM, data={'is_filled': False, 'parameter': parameter if type == SCATTER_MAP else None}),
        dcc.Store(id=SG_PARAM, data={'is_filled': False, 'parameter': parameter if type == SCATTER_GEO else None}),
        dcc.Store(id=D_PARAM, data={'is_filled': False, 'parameter': parameter if type == DENSITY else None}),
        dcc.Store(id=CH_PARAM, data={'is_filled': False, 'parameter': parameter if type == CHOROPLETH else None}),
        dcc.Store(id=CA_PARAM, data={'is_filled': False, 'parameter': parameter if type == CAROUSEL else None}),
        dcc.Store(id=BC_PARAM, data={'is_filled': False, 'parameter': parameter if type == BAR_CHART_RACE else None}),

        dbc.Form(
            options,
            inline=True,
            # style={'background':'red'}
        )
    ])




def parameter_option(name, id, multi = False):

    if not multi:
        dropdown = dbc.Select(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in collection.temp.columns],
        )
    else:
        dropdown = dcc.Dropdown(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in collection.temp.columns],
            multi= multi
        )
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label(name, className="mr-2"),
                        dropdown,
                    ],
                    # className="mr-3",
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
                    # className="mr-3",
                    style={'width': '50%', 'padding':'5px'}
        )


def dropdown_markup(measurements):
    return dbc.FormGroup(
        [
            dbc.Label('Choose a dataset', className="mr-2"),
            dbc.Select(
                style={'width': '100%'},
                id='dataset-dropdown',
                options=[{"label": i['name'], "value": i['name']} for i in measurements],
            )
        ],
        # className="mr-3",
        style={'width': '50%', 'padding':'5px'}
    )

def expression_box_markup(id):
    operators = ['+', '-',]
    if id != 0:
        operators.append('×')
        operators.append('÷')
    return html.Div(
        className='expression-box',
        children=[
            dbc.FormGroup(
                [
                    dbc.Label(f'Operator {id+1}',style={'fontSize':'10px'}  ),
                    dbc.Select(
                        id=f'operator-{id}',
                        options=[{"label": i, "value": i} for i in operators],
                        value = '+' if id == 0 else ''
                    ),

                ],
                # className="mr-3",
                className='operator',
            ),
            dbc.FormGroup(
                [
                    html.Div([
                        dbc.Label(f'Operand {id + 1}', style={'fontSize': '10px'}),
                        html.I(className="fa fa-list rotate-icon", id = f'operand-icon-{id}'),

                    ]
                        , className='operand-title'
                    ),
                    # dbc.Label(f'Operand {id + 1}', style={'fontSize': '10px'}),
                    # dcc.Store(id=f'operand-type-{id}', data='dropdown'),
                    html.Div(
                        id=f'operand-container-{id}',
                        children = operand_container_markup('dropdown', id)
                    ),

                ],
                className='operand',
            ),
        ], )

def operand_container_markup(type, id):
    if type == 'dropdown':
        return dbc.Select(
            id=f'operand-{id}',
            options=[{"label": i, "value": i} for i in collection.temp.columns],
        )
    elif type == 'number':
        return dbc.Input(
            id=f'operand-{id}',
            type = 'number',
            autoComplete='off',
            maxLength=8,
            # placeholder="A large input...", bs_size="lg", className="mb-3"
        )