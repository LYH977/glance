import dash

import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# Connect to main app.py file
from dash.exceptions import PreventUpdate

from app import app

from pages import homepage, dashboard, upload_page
from components import carousel
from layout.navbar import navbar
from utils import collection
from utils.method import reset_var, get_ctx_type, get_ctx_index

app.layout = html.Div([
    navbar,
    html.Div(id='page-content', children=[]),
    dbc.Modal(
                [
                    dbc.ModalHeader("Create New Visualization"),
                    dbc.ModalBody(html.Div([
                        dcc.Store(id='form-complete', data=False),
                        dcc.Upload(
                            id='upload-dataset',
                            children=html.Button('Upload File'),
                            multiple=True
                        ),
                        html.Div(id='preview'),
                        dbc.FormGroup(
                            [
                                dbc.Label("Choose Datetime column*", html_for="dropdown"),
                                dcc.Dropdown(
                                    id="dt-dropdown",
                                    disabled=True,
                                ),
                            ]
                        ),
                        html.Div(id='dt-modifier'),
                    ])),
                    dbc.ModalFooter(
                        html.Div([
                            dbc.Button("Upload", id="dt-upload", className="ml-auto", color="success", disabled=True),
                            dbc.Button("Cancel", id="cancel-upload", className="ml-auto", color="danger", ),

                        ])
                    ),
                ],
                id="upload-modal",
                size="xl",
                backdrop='static',
                is_open=False,
                autoFocus=False,

            ),
    html.Div(id='upload-toast')

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home' or pathname == '/':
        reset_var()
        return homepage.layout
    if pathname == '/pages/visualization':
        return dashboard.layout
    # if pathname == '/pages/upload':
    #     reset_var()
    #     return upload_page.layout
    else:
        return pathname


@app.callback(Output('upload-modal', 'is_open'),
              [Input('upload-button', 'n_clicks'), Input('cancel-upload', 'n_clicks')],
              State('upload-modal', 'is_open'),
              prevent_initial_call = True)
def update_output(open, close, is_open):
    # ctx = dash.callback_context
    # input_index = None
    # if not ctx.triggered:
    #     input_type = 'No input yet'
    # else:
    #     input_type = get_ctx_type(ctx)
    #     input_index = get_ctx_index(ctx)
    # if input_type =='upload-button' and open is not None:
    #     return True
    # elif input_type =='cancel-upload' and close is not None:
    #     return False
    # else:
    #     raise PreventUpdate
    return not is_open


if __name__ == '__main__':
    app.run_server(debug=True)
