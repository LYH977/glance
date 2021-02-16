import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from app import app
from utils.constant import FIGURE_TYPE
import base64
import io
import pandas as pd

dataset=[]
parameter=[]
modal = html.Div(
    [
        dbc.Button("Select File", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("Dataset Modal"),
                dbc.ModalBody(html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Button('Upload File'),
                        multiple=True
                    ),
                    html.Div(id='output-data-upload'),
                ])),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            size="xl",
            backdrop='static',

        ),
    ]
)


def parameter_option(name, id, multi = False):
    return  \
        dbc.FormGroup(
                    [
                        dbc.Label(name, className="mr-2"),
                        dcc.Dropdown(
                            style={'width': '100%'},
                            id=id,
                            options=[{"label": i, "value": i} for i in parameter],
                            multi = multi
                        ),
                    ],
                    # className="mr-3",
                    style={'width': '50%'}
        )


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    global dataset
    global parameter
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            dataset = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            dataset = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    parameter = dataset.columns
    return html.Div([
        html.H6(f'Filename: {filename}'),
        html.H6('Below are the first 5 rows.'),

        dash_table.DataTable(
            data=dataset.head(5).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in dataset.columns]
        ),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Visualization type", html_for="dropdown"),
                dcc.Dropdown(
                    id="visual-type",
                    options=[{"label": i, "value": j} for i, j in zip(FIGURE_TYPE.keys(), FIGURE_TYPE.values())],
                ),
            ]
        ),
        dbc.Form(
            [
                parameter_option('Latitude', 'latitude'),
                parameter_option('Longitude', 'longitude'),
                parameter_option('Size', 'size'),
                parameter_option('Color', 'color'),
                parameter_option('Animation Frame', 'anim_frame'),
                parameter_option('Additional Message', 'message', True),

            ],
            inline=True,
            # style={'background':'red'}
        )


    ])







@app.callback([Output('output-data-upload', 'children'),Output("modal", "is_open")],
              [Input("open", "n_clicks"), Input("close", "n_clicks"),Input('upload-data', 'contents')],
              [State('upload-data', 'filename'), State('upload-data', 'last_modified'),State("modal", "is_open")],
              prevent_initial_call=True
)
def update_output(n1, n2,list_of_contents, list_of_names, list_of_dates,is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'upload-data':
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children, dash.no_update

    elif input_id == 'open' or 'close':
        return dash.no_update if is_open is True else [],\
               not is_open

    else:
        raise PreventUpdate

