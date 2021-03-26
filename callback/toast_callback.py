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

       ],
       prevent_initial_call=True
    )
    def update_toast(upload, dashboard):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type == 'upload-toast' and upload is not None:
            return upload['children'], upload['is_open'], upload['icon'], upload['header']
        elif input_type == 'dashboard-toast' and dashboard is not None:
            return dashboard['children'], dashboard['is_open'], dashboard['icon'], dashboard['header']
        raise PreventUpdate