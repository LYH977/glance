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
import datetime
import io
import os
import pandas as pd

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
            backdrop='static'
        ),
    ]
)
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H6(f'Filename: {filename}'),
        html.H6('Below are the first 5 rows.'),

        dash_table.DataTable(
            data=df.head(5).to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Figure type", html_for="dropdown"),
                dcc.Dropdown(
                    id="figure-type",
                    options=[{"label": i, "value": j} for i, j in zip(FIGURE_TYPE.keys(), FIGURE_TYPE.values())],
                ),
            ]
        ),
        dbc.Form(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("Email", className="mr-2"),
                        dcc.Dropdown(
                            style={'width': '100%'},
                            id="figure-type",
                            options=[{"label": i, "value": j} for i, j in
                                     zip(FIGURE_TYPE.keys(), FIGURE_TYPE.values())],
                        ),                    ],
                    # className="mr-3",
                    style={'width': '50%'}

                ),
                dbc.FormGroup(
                    [
                        dbc.Label("Password", className="mr-2"),
                        dcc.Dropdown(
                            style={'width': '100%'},
                            id="figure-type",
                            options=[{"label": i, "value": j} for i, j in
                                     zip(FIGURE_TYPE.keys(), FIGURE_TYPE.values())],
                        ),                    ],
                    # className="mr-3",
                    style={'width': '50%'}
                ),
            ],
            inline=True,
            style={'background':'red'}
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

