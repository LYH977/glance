import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
import numexpr as ne
import numpy as np
from dash.exceptions import PreventUpdate

from components.carousel import create_ca_img
from database.dbConfig import client
from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM, SM_PARAM, CA_PARAM, CH_PARAM, D_PARAM, BC_PARAM, SG_PARAM, \
    CAROUSEL, CAROUSEL_CONSTANT, ITEM, FRAME, TIME, SCATTER_MAP, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE
from utils import collection
from utils.method import get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index, formatted_time_value, \
    select_query
from components.select_dataset_modal import output_form_markup, dataset_portal_markup, dataset_portal_markup, \
    dropdown_markup
import base64
import io
import json
import pandas as pd





def validate_create(data):
    ctx = dash.callback_context
    input_value = None
    if not ctx.triggered:
        input_type = 'No input yet'
        raise PreventUpdate
    else:
        input_type = get_ctx_type(ctx)
        input_value = get_ctx_value(ctx)
    data['parameter'][input_type] = input_value
    is_filled = False if None in data['parameter'].values() else True
    # print(data['parameter'])
    return {'is_filled': is_filled, 'parameter': data['parameter']}



#############################################################################################################################################


def register_update_after_upload(app):
    @app.callback(Output('dataset-portal', 'children'),
                  [
                      Input("open", "n_clicks"),
                      Input("cancel-create-visual", "n_clicks"),
                      Input("create-visual", "n_clicks"),
                      Input('chosen-dropdown', 'data')
                  ],
                  [State("modal", "is_open")],
                  prevent_initial_call=True
    )
    def update_after_upload(open, close, create, measurement, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_type == 'chosen-dropdown':
            if measurement is not None:
                collection.temp = select_query(measurement)
                if collection.temp is not None:
                    collection.temp['time'] = collection.temp.index.map(lambda x: str(x).split('+')[0])

                    # eq = "A + B "
                    # A = collection.temp['Latitude']
                    # B = collection.temp['Longitude']
                    # ne.evaluate(eq)

                    # df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
                    # eq = 'A +B'
                    # print(df.eval(eq))

                    # print(float(collection.temp['Latitude']) + float(collection.temp['Longitude']))

                return dataset_portal_markup(measurement)


        elif input_type == 'create-visual' or 'cancel-create-visual' :
            return dash.no_update if is_open is True else []

        # elif input_type ==  'create-visual':
        #     return  []
        else:
            raise PreventUpdate
#############################################################################################################################################


def register_update_output_form(app):
    @app.callback(Output('output-form', 'children'),
                  Input("visual-type", "value"),
                  prevent_initial_call=True
    )
    def update_output_form(type):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_type == 'visual-type' and type is not None:
            return output_form_markup(type)
        # elif input_type == 'close' or input_type == 'create':
        #     return None
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_toggle_modal(app):
    @app.callback(
        Output("modal", "is_open"),
        [Input("open", "n_clicks"), Input("cancel-create-visual", "n_clicks"),Input("create-visual", "n_clicks")],
        [State("modal", "is_open"), State('last-param', 'data')],
        prevent_initial_call=True
    )
    def toggle_modal (open, close, create, is_open, param):
        # print(param)
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = ctx.triggered[0]['prop_id'].split('.')[0]
        # if input_type == 'create-visual':
        #     if param['vtype'] == CAROUSEL:
        #         temp = []
        #         for row in collection.temp.index:
        #             temp.append( create_ca_img(collection.temp.loc[row, param['parameter'][CAROUSEL_CONSTANT[ITEM]]]) )
        #         collection.img_container[create] = temp
        # if open is  None:
        #     return dash.no_update
        return not is_open
#############################################################################################################################################


def register_enable_create_btn(app):
    @app.callback(
        [Output('create-visual', 'disabled'),  Output('last-param', 'data')] ,
        [
            Input(SM_PARAM,'data'),
            Input(SG_PARAM, 'data'),
            Input(D_PARAM, 'data'),
            Input(CH_PARAM, 'data'),
            Input(CA_PARAM, 'data'),
            Input(BC_PARAM, 'data'),
            Input('create-visual', 'n_clicks'),
        ],
        State('visual-type', 'value'),
        prevent_initial_call=True
    )
    def enable_create_btn (sm, sg, d, ch, ca, bc, create, vtype):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
            input_value=None
        else:
            input_type = get_ctx_type(ctx)
            input_value = get_ctx_value(ctx)

        if input_type == 'create-visual':
            return True, dash.no_update
        if input_value['parameter'] is not None and input_value['is_filled'] is True:
            data = {'vtype': vtype, 'parameter':input_value['parameter'] }
            return False, data
        else:
            raise PreventUpdate
#############################################################################################################################################


# def register_clear_upload(app):
#     @app.callback(
#         Output('upload-data', 'contents') ,
#         [Input('close','n_clicks'), Input('create','n_clicks')],
#         prevent_initial_call=True
#     )
#     def clear_upload (close,create):
#         return None

def register_update_dt_dropdown(app):
    @app.callback(
        Output('dataset-window', 'children') ,
        [Input('open','n_clicks'), Input('cancel-create-visual','n_clicks'), Input('create-visual','n_clicks')],
        prevent_initial_call=True
    )
    def update_dt_dropdown (open, close,create):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
            input_value=None
        else:
            input_type = get_ctx_type(ctx)
            input_value = get_ctx_value(ctx)
        if input_type == 'open':
            return dropdown_markup(client.get_list_measurements())
        elif input_type == 'cancel-create-visual' or 'create-visual':
            return None
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_update_chosen_dropdown(app):
    @app.callback(
        Output('chosen-dropdown', 'data') ,
        [Input('dataset-dropdown','value')],
        prevent_initial_call=True
    )
    def update_chosen_dropdown (value):
        return value

#############################################################################################################################################


def register_validate_sm_create(app):
    @app.callback(
        Output(SM_PARAM, 'data') ,
        [
            Input("sm_latitude", "value"),
            Input("sm_longitude", "value"),
            Input("sm_size", "value"),
            Input("sm_color", "value"),
            Input("sm_name", "value"),
            # Input("sm_frame", "value"),
            Input("sm_message", "value"),
        ],
        State(SM_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_sm_create (lat, long, size, color, name, msg, data):
        # print(data)
        return validate_create(data)


#############################################################################################################################################


def register_validate_sg_create(app):
    @app.callback(
        Output(SG_PARAM, 'data') ,
        [
            Input("sg_latitude", "value"),
            Input("sg_longitude", "value"),
            Input("sg_size", "value"),
            Input("sg_color", "value"),
            Input("sg_name", "value"),
            # Input("sg_frame", "value"),
            Input("sg_message", "value"),
        ],
        State(SG_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_sg_create (lat, long, size, color, name, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_bc_create(app):
    @app.callback(
        Output(BC_PARAM, 'data') ,
        [
            Input("bc_item", "value"),
            Input("bc_value", "value"),
            # Input("bc_frame", "value"),
        ],
        State(BC_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_bc_create (item, value, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_d_create(app):
    @app.callback(
        Output(D_PARAM, 'data') ,
        [
            Input("d_latitude", "value"),
            Input("d_longitude", "value"),
            Input("d_z", "value"),
            # Input("d_frame", "value"),
            Input("d_message", "value"),
        ],
        State(D_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_d_create (lat, long, z, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ch_create(app):
    @app.callback(
        Output(CH_PARAM, 'data') ,
        [
            Input("ch_locations", "value"),
            Input("ch_color", "value"),
            Input("ch_name", "value"),
            # Input("ch_frame", "value"),
            Input("ch_message", "value"),
        ],
        State(CH_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ch_create (loc, color, name, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ca_create(app):
    @app.callback(
        Output(CA_PARAM, 'data') ,
        [
            Input("ca_item", "value"),
            # Input("ca_frame", "value"),
        ],
        State(CA_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ca_create (item, data):
        return validate_create(data)


#############################################################################################################################################


def register_update_chosen_tformat(app):
    @app.callback(
        Output('chosen-tformat', 'data') ,
        Input("time-format", "value"),
        prevent_initial_call=True
    )
    def update_chosen_tformat (value):
        return value
#############################################################################################################################################

#
# def register_toggle_custom_column_collapse(app):
#     @app.callback(
#         Output("collapse", "is_open"),
#         [Input("collapse-button", "n_clicks")],
#         [State("collapse", "is_open")],
#     )
#     def toggle_custom_column_collapse(n, is_open):
#         if n:
#             return not is_open
#         return is_open