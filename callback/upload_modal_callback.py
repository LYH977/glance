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



def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            collection.temp = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            print('csv', collection.temp)
        elif 'xls' in filename:
            # Assume that the user uploaded an data file
            collection.temp = pd.read_excel(io.BytesIO(decoded))
            print('xls', collection.temp)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return preview_markup(filename)

#############################################################################################################################################


def register_update_preview(app):
    @app.callback([Output('preview', 'children'), Output('dt-dropdown-area', 'children')],
                  [Input('upload-dataset', 'contents'), Input('upload-button', 'n_clicks')],
                  [State('upload-dataset', 'filename'), State('upload-dataset', 'last_modified')],
                  prevent_initial_call=True
    )
    def update_preview(list_of_contents,close, list_of_names, list_of_dates):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type=='upload-dataset' and list_of_contents is not None:
            children = [
                parse_contents(c, n) for c, n in
                zip(list_of_contents, list_of_names)
            ]
            options = [{"label": i, "value": i} for i in collection.temp.columns]
            collection.temp = collection.temp.dropna()
            collection.temp = collection.temp.reset_index(drop=True)
            return children, dt_dropdown_markup(options)
        elif input_type =='upload-button':
            return None, None
        else:
            raise PreventUpdate
#############################################################################################################################################


def register_update_datetime_value(app):
    @app.callback(Output('datetime-value', 'data'),
                  Input('dt-dropdown', 'value'),
                  prevent_initial_call=True
    )
    def update_datetime_modifier(value):
        return value

#############################################################################################################################################


def register_update_datetime_modifier(app):
    @app.callback(Output('dt-modifier', 'children'),
                 [ Input('datetime-value', 'data'), Input('upload-dataset', 'contents'), Input('upload-button', 'n_clicks')],
                  prevent_initial_call=True
    )
    def update_datetime_modifier(value, contents, close):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type == 'datetime-value' and value is not None:
            # dt = collection.temp.loc[0, value]
            text_input = dt_modifier_markup(value)
            return text_input
        elif input_type == 'upload-dataset':
            return None
        elif input_type == 'upload-button':
            return None
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_update_datetime_filled(app):
    @app.callback(Output('dt-filled', 'data'),
                  [Input('dt-format', 'data'), Input('name-input', 'value')],
                  [State('dt-format', 'data'), State('name-input', 'value')],
                  prevent_initial_call=True
    )
    def update_datetime_filled(format, name, sformat, sname):
        return True if sformat is True and sname is not None and len(sname) > 0  else False


#############################################################################################################################################


def register_update_datetime_upload_btn(app):
    @app.callback(Output('confirm-upload', 'disabled'),
                  [Input('form-complete', 'data'), Input('upload-dataset', 'contents')],
                  prevent_initial_call=True
    )
    def update_datetime_upload_btn(value, contents):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type=='form-complete':
            return not value
        elif input_type =='upload-dataset':
            return True
        else:
            return PreventUpdate
#############################################################################################################################################


def register_update_datetime_format(app):
    @app.callback(Output('dt-format', 'data'),
                  Input('check-dt-format', 'n_clicks'),
                  [State('dt-input', 'value'), State('datetime-value', 'data')],
                  prevent_initial_call=True
    )
    def update_datetime_format(click, input, value):
        if click is not None:
            try:
                dt = collection.temp.loc[0, value]
                dt_obj = datetime.strptime(str(dt), input)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            raise PreventUpdate

#############################################################################################################################################

def register_update_form_complete(app):
    @app.callback(Output('form-complete', 'data'),
                  Input('dt-filled', 'data'),
                  prevent_initial_call=True
    )
    def uupdate_form_complete(value):
        return value

#############################################################################################################################################

def register_clear_dropdown(app):
    @app.callback(Output('dt-dropdown', 'value'),
                  Input('upload-dataset', 'contents'),
                  prevent_initial_call=True
    )
    def clear_dropdown(content):
        return None

#############################################################################################################################################

def register_clear_upload_content(app):
    @app.callback(Output('upload-dataset', 'contents'),
                  [Input('confirm-upload', 'n_clicks'), Input('cancel-upload', 'n_clicks')],
                  prevent_initial_call=True
    )
    def clear_upload_upload_content(confirm, cancel):
        return None
#############################################################################################################################################

def register_update_upload_modal(app):
    @app.callback(Output('upload-modal', 'is_open'),
              [
                  Input('upload-button', 'n_clicks'),
                  Input('confirm-upload', 'n_clicks'),
                  Input('cancel-upload', 'n_clicks'),
              ],
              State('upload-modal', 'is_open'),
              prevent_initial_call = True)
    def update_output(open, confirm, close, is_open):
        return not is_open
#############################################################################################################################################

def register_handle_upload_click(app):
    @app.callback(
       Output('upload-toast', 'data'),
       Input('confirm-upload', 'n_clicks'),
       [State('datetime-value', 'data'), State('dt-input', 'value'), State('name-input', 'value'), State('dt-tags', 'value')],
       prevent_initial_call=True
    )
    def update_handle_upload_click(click, dt, input, name, tags):
        dataset = collection.temp
        pd.options.mode.chained_assignment = None
        try:
            dataset[dt] = dataset[dt].map(lambda x : datetime.strptime(str(x), input).strftime('%Y-%m-%d %H:%M:%S.%f'))
            json_body = []
            fields = list(dataset)
            if tags:
                for t in tags:
                    fields.remove(t)
            fields.remove(dt)
            for count in range(len(dataset.index)):
                tag_obj = {}
                field_obj = {}
                if tags:
                    for t in tags:
                        tag_obj[t] = dataset.loc[count, t]
                for f in fields:
                    data =  dataset.loc[count, f]
                    field_obj[f] = data
                json_body.append({
                    "measurement":name,
                    "tags": tag_obj,
                    "time": dataset.loc[count, dt],
                    "fields" : field_obj
                })
            new_client.write_points(json_body, time_precision='ms')
            toast = {
                'children' : f'{name} is successfully added.',
                'is_open' : True,
                'icon' : 'success',
                'header' : 'SUCCESS'
            }
            return toast
        except Exception as e:
            print('error', e)
            toast = {
                'children': f'Error found in the dataset : {e}',
                'is_open': True,
                'icon': 'danger',
                'header': 'DANGER'
            }
            return toast
#############################################################################################################################################

def register_update_dt_input_validity(app):
    @app.callback([Output('dt-input', 'valid'), Output('dt-input', 'invalid')],
                  Input('dt-format', 'data'),
                  prevent_initial_call = True)
    def update_dt_input_validity(valid):
        return valid, not valid