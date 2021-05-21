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
from database.dbConfig import client
from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM, SM_PARAM, CA_PARAM, CH_PARAM, D_PARAM, BC_PARAM, SG_PARAM, \
    CAROUSEL, CAROUSEL_CONSTANT, ITEM, FRAME, TIME, SCATTER_MAP, NOTIFICATION_PARAM, TAG, FIELD, SCATTER_MAP_CONSTANT, \
    NAME, LATITUDE, LONGITUDE
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

#############################################################################################################################################


def register_toggle_open_edit_modal(app):
    @app.callback(
        [
            Output("edit-visual-modal", "is_open"),
            Output("modal-head", "children"),
            Output({'type': "last-edit-click-ts", 'index': ALL}, "data"),
        ],
        [
            Input({'type': "edit-visual-btn", 'index': ALL}, "n_clicks_timestamp"),
            Input("cancel-edit-visual", "n_clicks"),
            Input("edit-visual", "n_clicks"),
        ],
        State({'type': "last-edit-click-ts", 'index': ALL}, "data"),
        prevent_initial_call=True
    )
    def toggle_open_edit_modal(edit_ts, cancel, edit_visual, last_edit):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)

        if input_type == 'edit-visual-btn':
            for index, (first, second) in enumerate(zip(edit_ts, last_edit)):
                if first != second:
                    diff_index = get_ctx_index(ctx)
                    header = f'Edit Visual {diff_index}'
                    return  True, header, edit_ts

        elif input_type == 'cancel-edit-visual' and cancel >0:
            return False, dash.no_update, edit_ts
        elif input_type == 'edit-visual' and edit_visual >0:
            return False, dash.no_update, edit_ts
        raise PreventUpdate



#############################################################################################################################################


def register_validate_sm_create_edit_modal(app):
    @app.callback(
        Output(SM_PARAM, 'data') ,
        [
            Input("sm_latitude_edit_modal", "value"),
            Input("sm_longitude_edit_modal", "value"),
            Input("sm_size_edit_modal", "value"),
            Input("sm_color_edit_modal", "value"),
            Input("sm_name_edit_modal", "value"),
            # Input("sm_frame", "value"),
            Input("sm_message_edit_modal", "value"),
        ],
        State(SM_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_sm_create_edit_modal (lat, long, size, color, name, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_bc_create_edit_modal(app):
    @app.callback(
        Output(BC_PARAM, 'data') ,
        [
            Input("bc_item_edit_modal", "value"),
            Input("bc_value_edit_modal", "value"),
            # Input("bc_frame", "value"),
        ],
        State(BC_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_bc_create_edit_modal (item, value, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_d_create_edit_modal(app):
    @app.callback(
        Output(D_PARAM, 'data') ,
        [
            Input("d_latitude_edit_modal", "value"),
            Input("d_longitude_edit_modal", "value"),
            Input("d_z_edit_modal", "value"),
            # Input("d_frame", "value"),
            Input("d_message", "value"),
        ],
        State(D_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_d_create_edit_modal (lat, long, z, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ch_create_edit_modal(app):
    @app.callback(
        Output(CH_PARAM, 'data') ,
        [
            Input("ch_locations_edit_modal", "value"),
            Input("ch_color_edit_modal", "value"),
            Input("ch_name_edit_modal", "value"),
            # Input("ch_frame", "value"),
            Input("ch_message_edit_modal", "value"),
        ],
        State(CH_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ch_create_edit_modal (loc, color, name, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ca_create_edit_modal(app):
    @app.callback(
        Output(CA_PARAM, 'data') ,
        [
            Input("ca_item_edit_modal", "value"),
            # Input("ca_frame", "value"),
        ],
        State(CA_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ca_create_edit_modal (item, data):
        return validate_create(data)


#############################################################################################################################################


def register_update_chosen_tformat_edit_modal(app):
    @app.callback(
        Output('chosen-tformat_edit_modal', 'data') ,
        Input("time-format_edit_modal", "value"),
        prevent_initial_call=True
    )
    def update_chosen_tformat_edit_modal (value):
        return value