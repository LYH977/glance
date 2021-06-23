import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate
import math
from database.dbConfig import client
from utils.constant import FIGURE_OPTION, FIGURE_PARAM, CREATE_BTN_ID, SM_PARAM, SG_PARAM, D_PARAM, CA_PARAM, CH_PARAM, \
    BC_PARAM, SCATTER_MAP, DENSITY, CHOROPLETH, CAROUSEL, BAR_CHART_RACE, TIME_FORMAT, YEAR, SECONDARY_FIGURE_OPTION, \
    STANDARD_T_FORMAT
from utils import  collection
from utils.method import unpack_parameter
import base64
import io
import pandas as pd
from datetime import  datetime


modal = html.Div(
    [
        dcc.Store(id='last-param', data={}),
        dcc.Store(id='visual-type-data', data= None),
        dcc.Store(id='chosen-tformat', data= YEAR),
        dcc.Store(id='chosen-dropdown', data= None),
        dcc.Store(id=SM_PARAM, data={ 'parameter': {} }),
        dcc.Store(id=D_PARAM, data={ 'parameter': {} }),
        dcc.Store(id=CH_PARAM, data={ 'parameter':  {} }),
        dcc.Store(id=CA_PARAM, data={ 'parameter':  {} }),
        dcc.Store(id=BC_PARAM, data={ 'parameter':  {} }),
        dbc.Modal(
            [
                dbc.ModalHeader("Create New Visualization", id = 'modal-head'),
                dbc.ModalBody(html.Div([
                    html.Div(id='dataset-window'),
                    html.Div(id='dataset-portal'),
                ])),
                dbc.ModalFooter(
                    html.Div([
                        html.Div(id="add-secondary-area"),
                        dbc.Button(
                            "Create",
                            id="create-visual",
                            className="ml-auto",
                            color="success",
                            disabled=True,
                            # style={'display':'block'}
                        ),
                        dbc.Button("Close", id="cancel-create-visual", className="ml-auto",color="danger"),
                    ], className= 'mod-footer')
                ),
            ],
            id="modal",
            size="xl",
            backdrop='static',
            is_open=False,
            autoFocus=False,
            # style={'background': 'red'}
            contentClassName='select-modal-content'

        ),
    ],
    # style={    'position':'relative', 'width':'inherit', 'height':'inherit'}
)

def dataset_portal_markup(filename, is_secondary):
    return html.Div([

        html.Div(id='data-snapshot', children=snapshot_markup(filename, is_secondary)),
        html.Div(id='output-form'),
    ])



def snapshot_markup (filename, is_secondary):
    select_opt = SECONDARY_FIGURE_OPTION if is_secondary else FIGURE_OPTION
    suggestions = suggest_visual(is_secondary)

    return html.Div([
        html.Div([
            html.P(f'Below are random 5 rows:-'),
            dash_table.DataTable(
                id = 'portal-datatable',
                data = collection.temp.sample(n = 5).to_dict('records'),
                columns = [{'name': i, 'id': i} for i in collection.temp.columns],
                style_cell={
                    'textAlign': 'center',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    # 'maxWidth': 0
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }

            ),
            html.Div([
                html.I(className="fa fa-plus-square icon-btn icon-black", id="click-target", style={}),
                dbc.Popover(
                    [
                        dbc.PopoverHeader(
                            [
                                dcc.Input(
                                    id='new-column-name',
                                    type="text",
                                    maxLength=10,
                                    size='13',
                                    placeholder='Name'
                                ),
                                html.P(' =', className='equation-window'),
                                html.P('(Equation)', className='equation-window',
                                         id='equation-window'),

                            ],
                            style={'background':'grey'}
                        ),
                        dbc.PopoverBody(
                            [
                                dcc.Store(id=f'operand-type', data={ 0:'dropdown', 1:'dropdown', 2:'dropdown' }),
                                html.Div([    expression_box_markup(n) for n in range(0,3)  ], className='expression-wrapper' ),
                                dbc.Row([
                                    dbc.Col(dbc.Button( "Confirm", id="confirm-new-col", className="mb-3", color="primary", outline=True , disabled= True), width='auto'),
                                    dbc.Col(dbc.Button( "Reset", id="reset-new-col", className="mb-3", color="danger"  ), width='auto'),
                                ], justify='around', align='center'),

                            ],
                            # style={'background': 'lightgrey'}

                        ),
                    ],
                    id="create-new-col-popup",
                    target="click-target",
                    trigger="legacy",
                    placement= 'right'
                ),
            ]),
        ]
        , style={'overflow':'auto'}),
        suggestions,

        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Visualization type", html_for="dropdown"),
                dbc.Select(
                    id="visual-type",
                    options=[{"label": i, "value": i} for i in select_opt],
                )
            ]
        ),
    ])




def output_form_markup(type, is_secondary):
    parameter={}
    for p_id, p_info in FIGURE_PARAM[type].items():
        parameter[p_id] = p_info['value']
    options = [ parameter_option(i, j, FIGURE_PARAM[type],parameter, k) for i,j,k in unpack_parameter(FIGURE_PARAM[type]) ]
    if not is_secondary:
        options.append(time_format_option())
    return html.Div([
        dbc.Form(
            options,
            inline=True,
            # style={'background':'red'}
        )
    ])


def parameter_option(name, id, type, parameter, multi = False):
    columns = collection.temp.columns
    if multi:
        value =  []
        for col in columns:
            temp = col
            if any(e in temp.lower() for e in type[id]['hint']):
                value.append(col)
        parameter[id] = value
        dropdown = dcc.Dropdown(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            multi=multi,
            value=value
        )
    else:
        columns = filter_column(type[id]['is_numeric'], columns)
        # if type[id]['is_numeric']:
        #     filtered_columns = []
        #     for col in columns:
        #         if collection.temp.dtypes[col] != 'object':
        #             filtered_columns.append(col)
        #         else:
        #                 try:
        #                     x = float(collection.temp[col].iloc[0])
        #                     y = float(collection.temp[col].iloc[-1])
        #                     filtered_columns.append(col)
        #                 except ValueError:
        #                     print('non-numeric column')
        #     columns = filtered_columns
        value = None
        for col in columns:
            temp = col
            if any(e in temp.lower()  for e in type[id]['hint']):
                value = col
                parameter[id] = value
                break
        dropdown = dbc.Select(
            style={'width': '100%'},
            id=id,
            options=[{"label": i, "value": i} for i in columns],
            value=value
        )
    fWeight = 'bold' if name[-1] == '*' else 'normal'
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label(name, className="mr-2", style={'fontWeight':fWeight}),
                        dropdown,
                    ],
                    # className="mr-3",
                    style={'width': '50%', 'padding':'5px'}
        )

def time_format_option():
    pdd = collection.temp
    length = len(pdd.index)
    first_id = pdd.index[0]
    middle_id = pdd.index[math.floor(length/2)]
    last_id =  pdd.index[length-1]
    list = []
    for id in [first_id, middle_id, last_id]:
        obj = pdd.loc[id, 'time']
        if type(obj) is not str:
            obj = obj[0]
        lala = datetime.strptime(obj, STANDARD_T_FORMAT)
        list.append(lala)

    diff = []
    for index in range(1, len(list)):
        for period in ['year', 'month', 'day', 'hour', 'minute', 'second']:
            obj1 = eval(f'list[{index}-1].{period}')
            obj2 = eval(f'list[{index}].{period}')
            if obj1 != obj2 and period.upper() not in diff:
                diff.append(period.upper())
    value = YEAR
    for k in TIME_FORMAT.keys():
        if all(e in k for e in diff):
            value = TIME_FORMAT[k]
            break
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label('Time Format*', className="mr-2", style={'fontWeight':'bold'}),
                        dbc.Select(
                            style={'width': '100%'},
                            id='time-format',
                            options=[{"label": i, "value": j} for i, j in
                                     zip(TIME_FORMAT.keys(), TIME_FORMAT.values())],
                            value=value
                        )
                    ],
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
    operators = [{'label':'+', 'value':'+'}, {'label':'-', 'value':'-'},]
    if id != 0:
        operators.append({'label':'×', 'value':'*'})
        operators.append({'label':'÷', 'value':'/'})
    return html.Div(
        className='expression-box',
        children=[
            dbc.FormGroup(
                [
                    dbc.Label(f'Operator {id+1}',style={'fontSize':'10px'}  ),
                    dbc.Select(
                        id=f'operator-{id}',
                        options=[{"label": i['label'], "value": i['value']} for i in operators],
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
                    html.Div(
                        id=f'operand-container-{id}',
                        children = operand_container_markup('dropdown', id)
                    ),
                ],
                className='operand',
            ),
            html.I(className="fa fa-undo undo-icon", id=f'exp-undo-{id}'),

        ], )

def operand_container_markup(type, id):
    filtered_col = filter_column(True, collection.temp.columns)
    if type == 'dropdown':
        return dbc.Select(
            id=f'operand-{id}',
            options=[{"label": i, "value": i} for i in filtered_col],
        )
    elif type == 'number':
        return dbc.Input(
            id=f'operand-{id}',
            type = 'number',
            autoComplete='off',
            maxLength=8,
            # placeholder="A large input...", bs_size="lg", className="mb-3"
        )

def secondary_action_btn_markup(create_click):
    return dbc.Button(
        'Create',
        id = {'type':'secondary-action-btn', 'index':create_click},
        className="ml-auto",
        color="success",
        n_clicks= 0,
        disabled= True
    )

def suggest_visual(is_secondary):
    visuals = FIGURE_OPTION if not is_secondary else SECONDARY_FIGURE_OPTION
    suggestions = []
    columns = collection.temp.columns

    for vis in visuals:     #density, scatter, choropleth..
        type = FIGURE_PARAM[vis]            # SCATTER_MAP_PARAM
        total_param = len(type)
        no_matched = 0
        for param in type.values():     #{ 'label':'Latitude*', 'value': None , 'multi': False, 'hint':['lat', 'latitude'] },

            for col in columns:
               temp = col
               if any(word in temp.lower() for word in param['hint']):
                   no_matched += 1
                   break
        mark =  float("{:.2f}".format(no_matched /total_param ))
        if mark > 0:
            suggestions.append(vis)
    if len(suggestions) == 0:
        return html.P('')
    else:
        suggestion = ', '.join([str(elem) for elem in suggestions])
        return dcc.Markdown(f'''
Suggestion: *__{suggestion}__*
''')


def filter_column(is_numeric, columns):
    if is_numeric:
        filtered_columns = []
        for col in columns:
            if collection.temp.dtypes[col] != 'object':
                filtered_columns.append(col)
            else:
                try:
                    x = float(collection.temp[col].iloc[0])
                    y = float(collection.temp[col].iloc[-1])
                    filtered_columns.append(col)
                except ValueError:
                    print('non-numeric column')
        return filtered_columns
    return columns
