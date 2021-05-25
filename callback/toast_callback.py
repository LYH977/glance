from datetime import datetime

import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash
from dash.exceptions import PreventUpdate

from database.dbConfig import new_client
from components.upload_modal import preview_markup, dt_modifier_markup, dt_dropdown_markup
from utils import collection
from utils.method import get_ctx_type, get_ctx_index
import base64
import io
import pandas as pd

# def give_toast_info(data):
#     return data['children'], data['is_open'], data['icon'], data['header']


def register_update_toast(app):
    @app.callback(
        [
            Output('my-toast', 'children'),
            Output('my-toast', 'is_open'),
            Output('my-toast', 'icon'),
            Output('my-toast', 'header'),
            Output({'type': "last-edit-toast", 'index': ALL}, "data"),
       ],
       [
           Input('upload-toast', 'data'),
           Input('dashboard-toast', 'data'),
           Input('create-new-column-toast', 'data'),
           Input({'type': 'edit-toast', 'index': ALL}, 'data'),

       ],
        State({'type': "last-edit-toast", 'index': ALL}, "data"),
       prevent_initial_call=True
    )
    def update_toast(upload, dashboard,new_column, edit, last_edit):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
        print('input_type',input_type)
        if input_type == 'upload-toast' and upload is not None:
            return upload['children'], upload['is_open'], upload['icon'], upload['header'], [x for x in edit]

        elif input_type == 'dashboard-toast' and dashboard is not None:
            return dashboard['children'], dashboard['is_open'], dashboard['icon'], dashboard['header'], [x for x in edit]

        elif input_type == 'create-new-column-toast' and new_column is not None:
            return new_column['children'], new_column['is_open'], new_column['icon'], new_column['header'], [x for x in edit]

        elif input_type == 'edit-toast' :
            print('edit', edit)
            for index, (first, second) in enumerate(zip(edit, last_edit)):
                if first != second:
                    return first['children'], first['is_open'], first['icon'], first['header'], [x for x in edit]
        raise PreventUpdate