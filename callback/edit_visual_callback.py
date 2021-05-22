import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_table
import dash
import numexpr as ne
import numpy as np
from dash.exceptions import PreventUpdate

from components.carousel import create_ca_img
from components.edit_visual_modal import edit_visual_portal_markup
from database.dbConfig import client
from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM, SM_PARAM, CA_PARAM, CH_PARAM, D_PARAM, BC_PARAM, SG_PARAM, \
    CAROUSEL, CAROUSEL_CONSTANT, ITEM, FRAME, TIME, SCATTER_MAP, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE, BAR_CHART_RACE, DENSITY, CHOROPLETH, EDIT_MODAL
from utils import collection
from utils.method import get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index, formatted_time_value, \
    select_query
from components.select_dataset_modal import output_form_markup, dataset_portal_markup, dataset_portal_markup, \
    dropdown_markup, operand_container_markup, secondary_action_btn_markup
import base64
import io
import json
import pandas as pd
from datetime import  datetime
import time



def assign_param(data, type):
    ctx = dash.callback_context
    input_value = None
    if not ctx.triggered:
        input_type = 'No input yet'
        raise PreventUpdate
    else:
        input_type = get_ctx_type(ctx)
        input_value = get_ctx_value(ctx)
    input_type = input_type.replace(EDIT_MODAL, '')
    data['parameter'][input_type] = input_value
    # data['type'] = type
    # print(data['parameter'])
    return data['parameter']

#############################################################################################################################################


def register_toggle_open_edit_modal(app):
    @app.callback(
        [
            Output("edit-visual-modal", "is_open"),
            Output("edit-modal-head", "children"),
            Output("edit-visual-portal", "children"),
            Output({'type': "last-edit-click-ts", 'index': ALL}, "data"),
        ],
        [
            Input({'type': "edit-visual-btn", 'index': ALL}, "n_clicks_timestamp"),
            Input("cancel-edit-visual", "n_clicks"),
            Input("confirm-edit-visual", "n_clicks"),
        ],
        [
            State({'type': "last-edit-click-ts", 'index': ALL}, "data"),
            State({'type': "my_param", 'index': ALL}, "data"),
            State({'type': "frame-format", 'index': ALL}, "data"),
            State({'type': "dataset-column-name", 'index': ALL}, "data"),
            State("param-to-edit", "data"),
        ],
        prevent_initial_call=True
    )
    def toggle_open_edit_modal(edit_ts, cancel, confirm, last_edit, old_param, tformat, columns, param_to_edit):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)
        if input_type == 'edit-visual-btn':
            for index, (first, second) in enumerate(zip(edit_ts, last_edit)):
                if first != second:
                    diff_index = get_ctx_index(ctx)
                    header = f'Edit Visual {diff_index} ({old_param[index]["vtype"]})'
                    return  True, header, edit_visual_portal_markup(old_param[index], columns[index], tformat[index]), edit_ts

        elif input_type == 'cancel-edit-visual' and cancel >0:
            return False, dash.no_update, None, edit_ts
        elif input_type == 'confirm-edit-visual' and confirm >0:
            print('b',param_to_edit)
            return False, dash.no_update, None, edit_ts
        raise PreventUpdate



#############################################################################################################################################


def register_validate_sm_create_edit_modal(app):
    @app.callback(
        Output(SM_PARAM+EDIT_MODAL, 'data') ,
        [
            Input("sm_latitude_edit_modal", "value"),
            Input("sm_longitude_edit_modal", "value"),
            Input("sm_size_edit_modal", "value"),
            Input("sm_color_edit_modal", "value"),
            Input("sm_name_edit_modal", "value"),
            # Input("sm_frame", "value"),
            Input("sm_message_edit_modal", "value"),
        ],
        State(SM_PARAM+EDIT_MODAL, 'data'),
        prevent_initial_call=True
    )
    def validate_sm_create_edit_modal (lat, long, size, color, name, msg, data):
        return assign_param(data, SCATTER_MAP)


#############################################################################################################################################


def register_validate_bc_create_edit_modal(app):
    @app.callback(
        Output(BC_PARAM+EDIT_MODAL, 'data') ,
        [
            Input("bc_item_edit_modal", "value"),
            Input("bc_value_edit_modal", "value"),
            # Input("bc_frame", "value"),
        ],
        State(BC_PARAM+EDIT_MODAL, 'data'),
        prevent_initial_call=True
    )
    def validate_bc_create_edit_modal (item, value, data):
        return assign_param(data, BAR_CHART_RACE)


#############################################################################################################################################


def register_validate_d_create_edit_modal(app):
    @app.callback(
        Output(D_PARAM+EDIT_MODAL, 'data') ,
        [
            Input("d_latitude_edit_modal", "value"),
            Input("d_longitude_edit_modal", "value"),
            Input("d_z_edit_modal", "value"),
            Input("d_message_edit_modal", "value"),
        ],
        State(D_PARAM+EDIT_MODAL, 'data'),
        prevent_initial_call=True
    )
    def validate_d_create_edit_modal (lat, long, z, msg, data):
        return assign_param(data, DENSITY)


#############################################################################################################################################


def register_validate_ch_create_edit_modal(app):
    @app.callback(
        Output(CH_PARAM+EDIT_MODAL, 'data') ,
        [
            Input("ch_locations_edit_modal", "value"),
            Input("ch_color_edit_modal", "value"),
            Input("ch_name_edit_modal", "value"),
            # Input("ch_frame", "value"),
            Input("ch_message_edit_modal", "value"),
        ],
        State(CH_PARAM+EDIT_MODAL, 'data'),
        prevent_initial_call=True
    )
    def validate_ch_create_edit_modal (loc, color, name, msg, data):
        return assign_param(data, CHOROPLETH)


#############################################################################################################################################


def register_validate_ca_create_edit_modal(app):
    @app.callback(
        Output(CA_PARAM+EDIT_MODAL, 'data') ,
        [
            Input("ca_item_edit_modal", "value"),
            # Input("ca_frame", "value"),
        ],
        State(CA_PARAM+EDIT_MODAL, 'data'),
        prevent_initial_call=True
    )
    def validate_ca_create_edit_modal (item, data):
        return assign_param(data, CAROUSEL)


#############################################################################################################################################


def register_update_chosen_tformat_edit_modal(app):
    @app.callback(
        Output('chosen-tformat_edit_modal', 'data') ,
        Input("time-format_edit_modal", "value"),
        prevent_initial_call=True
    )
    def update_chosen_tformat_edit_modal (value):
        return value
#############################################################################################################################################


def register_assign_param_to_edit(app):
    @app.callback(
        [
            Output('param-to-edit', 'data'),
        ] ,
        [
            Input(SM_PARAM+EDIT_MODAL,'data'),
            # Input(SG_PARAM, 'data'),
            Input(D_PARAM+EDIT_MODAL, 'data'),
            Input(CH_PARAM+EDIT_MODAL, 'data'),
            Input(CA_PARAM+EDIT_MODAL, 'data'),
            Input(BC_PARAM+EDIT_MODAL, 'data'),

        ],
        # [
        #     State({'type': 'secondary-action-btn', 'index': ALL}, 'disabled')
        # ],
        prevent_initial_call=True
    )
    def enable_create_btn (sm,  d, ch, ca, bc, ):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        else:
            input_type = get_ctx_type(ctx)
            input_value = get_ctx_value(ctx)

        print('a ',input_value)
        if input_value['parameter'] is not None :
            # data = {'vtype': vtype, 'parameter':input_value['parameter'] }

            return input_value
        raise PreventUpdate

#############################################################################################################################################


def register_toggle_edit_btn(app):
    @app.callback(
        Output('confirm-edit-visual', 'disabled') ,
        Input("param-to-edit", "data"),
        prevent_initial_call=True
    )
    def toggle_edit_btn (data):
        return True if len(data) == 0 else False

#############################################################################################################################################


# def register_toggle_param_to_edit(app):
#     @app.callback(
#         Output('param-to-edit', 'data') ,
#         Input("param-to-edit", "data"),
#         prevent_initial_call=True
#     )
#     def toggle_edit_btn (data):
#         return True if len(data) == 0 else False