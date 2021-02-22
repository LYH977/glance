import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM
from utils import collection
from components.upload_modal import output_form_markup,snapshot_markup
import base64
import io
import pandas as pd







#############################################################################################################################################

def parse_contents(contents, filename, date):
    print(7)

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
    return snapshot_markup(filename)

#############################################################################################################################################

def register_update_option(app):
    @app.callback( [ Output("parameter", "data"), Output('is-filled', 'data')],
                [
                    Input("latitude", "value"),
                    Input("longitude", "value"),
                    Input("size", "value"),
                    Input("color", "value"),
                    Input("name", "value"),
                    Input("frame", "value"),
                    Input("message", "value"),
                    Input('visual-type','value')
                ],
                    State("parameter", "data"),
                    prevent_initial_call=True
    )
    def update_option(lat, long, size, color, name, frame, msg, visual,param):
        ctx = dash.callback_context
        print(6)

        input_value = None
        if not ctx.triggered:
            input_id = 'No input yet'
            raise PreventUpdate
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
            input_value = ctx.triggered[0]['value']
        print(input_id,'in update_option')
        param[input_id] = input_value
        is_filled = False if None in param.values() and visual is None else True
        return  param, is_filled


#############################################################################################################################################




def register_update_data_snapshot(app):
    @app.callback(Output('data-snapshot', 'children'),
                  [Input("open", "n_clicks"), Input("close", "n_clicks"),Input("create", "n_clicks"), Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'), State('upload-data', 'last_modified'),State("modal", "is_open")],
                  prevent_initial_call=True
    )
    def update_data_snapshot(n1, n2,n3,list_of_contents, list_of_names, list_of_dates,is_open):
        ctx = dash.callback_context
        print(5)

        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_id == 'upload-data':
            if list_of_contents is not None:
                children = [
                    parse_contents(c, n, d) for c, n, d in
                    zip(list_of_contents, list_of_names, list_of_dates)]
                return children
        elif input_id == 'open' or 'close' :
            return dash.no_update if is_open is True else []
        elif input_id ==  'create':
            return  []
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_update_output_form(app):
    @app.callback(Output('output-form', 'children'),
                  [Input("visual-type", "value"), Input('close','n_clicks'), Input('create','n_clicks')],
                  prevent_initial_call=True
    )
    def update_output_form(type, close, create):
        print(1)
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(input_id)
        if input_id == 'visual-type' and type is not None:
            print('?')
            return output_form_markup(type)
        elif input_id == 'close' or input_id == 'create':
            return None
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_toggle_modal(app):
    @app.callback(
        Output("modal", "is_open"),
        [Input("open", "n_clicks"), Input("close", "n_clicks"),Input("create", "n_clicks")],
        State("modal", "is_open"),
        prevent_initial_call=True
    )
    def toggle_modal (open, close, create, is_open):
        print(2)

        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_id == 'create':
            collection.data[create] = collection.temp.dropna()
        return not is_open
#############################################################################################################################################


def register_enable_create_btn(app):
    @app.callback(
        Output('create', 'disabled') ,
        Input('is-filled','data'),
        prevent_initial_call=True
    )
    def enable_create_btn (is_filled):
        print(3)

        return not is_filled
#############################################################################################################################################


def register_clear_upload(app):
    @app.callback(
        Output('upload-data', 'contents') ,
        [Input('close','n_clicks'), Input('create','n_clicks')],
        prevent_initial_call=True
    )
    def clear_upload (close,create):
        print(4)

        return None

