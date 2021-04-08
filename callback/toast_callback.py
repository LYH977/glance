from datetime import datetime

import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
from dash.exceptions import PreventUpdate

from database.dbConfig import new_client
from components.upload_modal import preview_markup, dt_modifier_markup, dt_dropdown_markup
from utils import collection
from utils.method import get_ctx_type
import base64
import io
import pandas as pd

def give_toast_info(data):
    return data['children'], data['is_open'], data['icon'], data['header']


def register_update_toast(app):
    @app.callback(
        [
            Output('my-toast', 'children'),
            Output('my-toast', 'is_open'),
            Output('my-toast', 'icon'),
            Output('my-toast', 'header'),
       ],
       [
           Input('upload-toast', 'data'),
           Input('dashboard-toast', 'data'),
           Input('create-new-column-toast', 'data'),

       ],
       prevent_initial_call=True
    )
    def update_toast(upload, dashboard,new_column):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type == 'upload-toast' and upload is not None:
            return give_toast_info(upload)
        elif input_type == 'dashboard-toast' and dashboard is not None:
            return give_toast_info(dashboard)
        elif input_type == 'create-new-column-toast' and new_column is not None:
            return give_toast_info(new_column)
        raise PreventUpdate