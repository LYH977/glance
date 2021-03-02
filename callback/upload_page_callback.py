from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from database.dbConfig import client, new_client
from pages.upload_page import preview_markup, dt_modifier_markup
from components.carousel import create_ca_img
from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM, SM_PARAM, CA_PARAM, CH_PARAM, D_PARAM, BC_PARAM, SG_PARAM, \
    CAROUSEL, CAROUSEL_CONSTANT, ITEM
from utils import collection
from utils.method import get_ctx_type,get_ctx_property,get_ctx_value,get_ctx_index
from components.select_dataset_modal import output_form_markup,dataset_portal_markup, dataset_portal_markup
import base64
import io
import json
import pandas as pd



def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            collection.temp = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an data file
            collection.temp = pd.read_data(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return preview_markup(filename)

#############################################################################################################################################


def register_update_preview(app):
    @app.callback([Output('preview', 'children'), Output('dt-dropdown', 'options'),  Output('dt-dropdown', 'disabled')],
                  Input('upload-dataset', 'contents'),
                  [State('upload-dataset', 'filename'), State('upload-dataset', 'last_modified')],
                  prevent_initial_call=True
    )
    def update_preview(list_of_contents,list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [
                parse_contents(c, n) for c, n in
                zip(list_of_contents, list_of_names)
            ]
            options = [{"label": i, "value": i} for i in collection.temp.columns]
            print('b', len( collection.temp.index))
            collection.temp = collection.temp.dropna()
            collection.temp = collection.temp.reset_index(drop=True)

            print('a',len( collection.temp.index))

            return children, options, False
        else:
            raise PreventUpdate


#############################################################################################################################################


def register_update_datetime_modifier(app):
    @app.callback(Output('dt-modifier', 'children'),
                 [ Input('dt-dropdown', 'value'), Input('upload-dataset', 'contents')],
                  prevent_initial_call=True
    )
    def update_datetime_modifier(value, contents):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type == 'dt-dropdown':
            # dt = collection.temp.loc[0, value]
            text_input = dt_modifier_markup(value)
            return text_input
        elif input_type == 'upload-dataset':
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
        # ctx = dash.callback_context
        # if not ctx.triggered:
        #     input_type = 'No input yet'
        # else:
        #     input_type = get_ctx_type(ctx)
        #
        # if input_type == 'dt-format':
        #
        # elif input_type == 'upload-dataset':
        #     return False
        # else:
        #     raise PreventUpdate
        return True if sformat is True and len(sname) > 0  else False

#############################################################################################################################################


def register_update_datetime_upload_btn(app):
    @app.callback(Output('dt-upload', 'disabled'),
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
                  [State('dt-input', 'value'), State('dt-dropdown', 'value')],
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

def register_handle_upload_click(app):
    @app.callback(Output('upload-toast', 'children'),
                  Input('dt-upload', 'n_clicks'),
                  [State('dt-dropdown', 'value'), State('dt-input', 'value'), State('name-input', 'value'), State('dt-tags', 'value')],
                  prevent_initial_call=True
    )
    def update_handle_upload_click(click, dt, input, name, tags):
        dataset = collection.temp
        pd.options.mode.chained_assignment = None
        dataset[dt] = dataset[dt].map(lambda x : datetime.strptime(str(x), input).strftime('%Y-%m-%d %H:%M:%S.%f'))

        json_body = []
        fields = list(dataset)
        for t in tags:
            fields.remove(t)
        fields.remove(dt)

        for count in range(len(dataset.index)):
            print(count,' ',  dataset.loc[count, 'Item'], ' ',  dataset.loc[count, 'Year Code'])
            tag_obj = {}
            field_obj = {}
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
        # print(json_body)
        new_client.write_points(json_body)

        # dataset.set_index(dt, inplace= True)
        # dataset.index = pd.to_datetime(dataset.index)
        # print(dataset)
        # client.write_points(dataset, name, tag_columns=tags, protocol= 'line', numeric_precision= 'full')
        return 1