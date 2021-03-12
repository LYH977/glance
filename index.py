import dash

import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc

# Connect to main app.py file
from dash.exceptions import PreventUpdate

from app import app

from pages import homepage, dashboard, upload_modal
from components import carousel
from layout.navbar import navbar

from utils import collection
from utils.method import reset_var, get_ctx_type, get_ctx_index

app.layout = html.Div([
    navbar,
    html.Div(id='page-content', children=[]),
    upload_modal.layout

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home' or pathname == '/':
        reset_var()
        return homepage.layout
    if pathname == '/pages/visualization':
        return dashboard.layout
    else:
        return pathname


# @app.callback(Output('upload-modal', 'is_open'),
#               [Input('upload-button', 'n_clicks'), Input('cancel-upload', 'n_clicks')],
#               State('upload-modal', 'is_open'),
#               prevent_initial_call = True)
# def update_output(open, close, is_open):
#     return not is_open


if __name__ == '__main__':
    app.run_server(debug=True)
