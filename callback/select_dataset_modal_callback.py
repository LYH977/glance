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


def toggle_operand_type(type, id):
    if type == 'dropdown':
        classname = "fa fa-list-ol rotate-icon"
        type = 'number'
        child = operand_container_markup(type, id)

    else:
        classname = "fa fa-list rotate-icon"
        type = 'dropdown'
        child = operand_container_markup(type, id)

    return type, classname, child

def append_numeric_col_list(info, col):
    if col not in info['numeric_col']:
        info['numeric_col'].append(col)

#############################################################################################################################################


def register_update_after_upload(app):
    @app.callback(Output('dataset-portal', 'children'),
                  [
                      Input("open-select-modal", "n_clicks"),
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
                return dataset_portal_markup(measurement)


        elif input_type == 'create-visual' or 'cancel-create-visual' :
            # return dash.no_update if is_open is True else []
            time.sleep(1)
            return []

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
            return None
            # raise PreventUpdate

#############################################################################################################################################


# def register_toggle_modal(app):
#     @app.callback(
#         [
#             Output("modal", "is_open"),
#             Output({'type': "last-secondary-click-ts", 'index': ALL}, "data"),
#         ],
#         [
#             Input("open-select-modal", "n_clicks"),
#             Input("cancel-create-visual", "n_clicks"),
#             Input("create-visual", "n_clicks"),
#             Input({'type': "secondary-visual-btn", 'index': ALL}, "n_clicks_timestamp"),
#
#         ],
#         [
#             State("modal", "is_open"),
#             State({'type': "last-secondary-click-ts", 'index': ALL}, "data"),
#
#         ],
#         prevent_initial_call=True
#     )
#     def toggle_modal (open, close, create, secondary, is_open, last_secondary):
#         ts = datetime.now().timestamp()
#         ctx = dash.callback_context
#         if not ctx.triggered:
#             raise PreventUpdate
#         input_type = get_ctx_type(ctx)
#         if input_type == 'secondary-visual-btn':
#             for index, (first, second) in enumerate(zip(secondary, last_secondary)):
#                 if first != second:
#                     diff_index = get_ctx_index(ctx)
#                     return True, secondary
#                     break
#
#             raise PreventUpdate
#         else:
#             return not is_open, secondary

# test = [{'prop_id': '{"index":1,"type":"secondary-visual-btn"}.n_clicks_timestamp', 'value': 1621005249117}, {'prop_id': '{"index":2,"type":"secondary-visual-btn"}.n_clicks_timestamp', 'value': 1621005270133}, {'prop_id': '{"index":3,"type":"secondary-visual-btn"}.n_clicks_timestamp', 'value': None}]
#############################################################################################################################################


def register_toggle_modal_action_btn(app):
    @app.callback(
        [
            Output("create-visual", "style"),
            Output("add-secondary-area", "children"),
            Output("modal", "is_open"),
            Output("modal-head", "children"),
            Output({'type': "last-secondary-click-ts", 'index': ALL}, "data"),
        ],
        [
            Input("open-select-modal", "n_clicks"),
            Input("cancel-create-visual", "n_clicks"),
            Input("create-visual", "n_clicks"),
            Input({'type': "secondary-visual-btn", 'index': ALL}, "n_clicks_timestamp"),
        ],
        [
            State("modal", "is_open"),
            State({'type': "last-secondary-click-ts", 'index': ALL}, "data"),

        ],
        prevent_initial_call=True
    )
    def toggle_modal_action_btn (open, close, create, secondary, is_open, last_secondary):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)

        if input_type == 'secondary-visual-btn':
            style = {'display': 'none'}
            # input_index = get_ctx_index(ctx)
            for index, (first, second) in enumerate(zip(secondary, last_secondary)):
                if first != second:
                    diff_index = get_ctx_index(ctx)
                    header = f'Add Secondary Layer for Visual {diff_index}'
                    return style, secondary_action_btn_markup(diff_index), True, header, secondary
            raise PreventUpdate
        if input_type == 'cancel-create-visual':
            header = dash.no_update
        else:
            header = 'Create Visualization'
        style = {'display':'block'}

        return style, [], not is_open, header, secondary
#############################################################################################################################################


def register_enable_create_btn(app):
    @app.callback(
        [
            Output('create-visual', 'disabled'),
            Output('last-param', 'data')
        ] ,
        [
            Input(SM_PARAM,'data'),
            # Input(SG_PARAM, 'data'),
            Input(D_PARAM, 'data'),
            Input(CH_PARAM, 'data'),
            Input(CA_PARAM, 'data'),
            Input(BC_PARAM, 'data'),
            Input('create-visual', 'n_clicks'),
        ],
        State('visual-type', 'value'),
        prevent_initial_call=True
    )
    def enable_create_btn (sm,  d, ch, ca, bc, create, vtype):
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
        [
            Input('open-select-modal','n_clicks'),
            Input('cancel-create-visual','n_clicks'),
            Input('create-visual','n_clicks')
        ],
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
        if input_type == 'open-select-modal':
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
        return validate_create(data)


#############################################################################################################################################


# def register_validate_sg_create(app):
#     @app.callback(
#         Output(SG_PARAM, 'data') ,
#         [
#             Input("sg_latitude", "value"),
#             Input("sg_longitude", "value"),
#             Input("sg_size", "value"),
#             Input("sg_color", "value"),
#             Input("sg_name", "value"),
#             # Input("sg_frame", "value"),
#             Input("sg_message", "value"),
#         ],
#         State(SG_PARAM, 'data'),
#         prevent_initial_call=True
#     )
#     def validate_sg_create (lat, long, size, color, name, msg, data):
#         return validate_create(data)


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


def register_update_equation(app):
    @app.callback(
        Output("equation-window", "children"),
        [
            # Input("new-column-name", "value"),
            Input('operator-0', "value"),
            Input('operator-1', "value"),
            Input('operator-2', "value"),
            Input('operand-0', "value"),
            Input('operand-1', "value"),
            Input('operand-2', "value"),
        ],
        prevent_initial_call=True

    )
    def update_equation( op1, op2, op3, or1, or2, or3):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)


        operator1 = op1 if op1 == '-' else ''
        operand1 = or1 if or1 is not None else ''

        operator2 = op2 if op2 is not None else ''
        operand2 = or2 if or2 is not None else ''

        operator3 = op3 if op3 is not None else ''
        operand3 = or3 if or3 is not None else ''

        operation1 = f'{operator1}{operand1}' if operand1 != '' else ''  # A/-A
        operation2 = f'{operator2} {operand2}' if operator2 != '' and operand2 != '' else '' # +B/-B
        operation3 = f'{operator3} {operand3}'  if operator3 != '' and operand3 != '' else ''# +C/-C
        equation = f'{operation1} {operation2} {operation3}'
        return '(Equation will appear here)' if not equation or equation.isspace() else equation



#############################################################################################################################################


def register_update_new_column(app):
    @app.callback(
        [
            Output('portal-datatable', 'data'),
            Output('portal-datatable', 'columns'),
            Output('create-new-column-toast', 'data'),

        ] ,
        [
            Input("confirm-new-col", "n_clicks"),

        ],
        [
            State("equation-window", "children"),
            State("operand-type", "data"),
            State("operand-0", "value"),
            State("operand-1", "value"),
            State("operand-2", "value"),
            State("new-column-name", "value"),

        ],
        prevent_initial_call=True
    )
    def update_new_column(click, eq, type,  od1, od2, od3, name):


        if click:
            if name in collection.temp.columns:
                toast = {
                    'children': f"Column name '{name}' already existed! Please use another name",
                    'is_open': True,
                    'icon': 'danger',
                    'header': 'DANGER'
                }
                return dash.no_update, dash.no_update,
            if eq == '(Equation will appear here)':
                toast = {
                    'children': 'No operator/operand selected',
                    'is_open': True,
                    'icon': 'danger',
                    'header': 'DANGER'
                }
                return dash.no_update, dash.no_update, toast
            try:
                copydf = collection.temp.copy(deep=True)
                if type['0'] == 'dropdown' and od1 is not None:
                    copydf[od1] = pd.to_numeric(copydf[od1])
                    append_numeric_col_list(collection.new_col, od1)

                if type['1'] == 'dropdown' and od2 is not None:
                    copydf[od2] = pd.to_numeric(copydf[od2])
                    append_numeric_col_list(collection.new_col, od2)

                if type['2'] == 'dropdown' and od3 is not None:
                    copydf[od3] = pd.to_numeric(copydf[od3])
                    append_numeric_col_list(collection.new_col, od3)

                new_col = copydf.eval(eq)
                collection.temp[name] = new_col
                collection.new_col['expression'].append({
                    'name': name,
                    'equation': eq
                })
                data = collection.temp.head(5).to_dict('records')
                columns = [{'name': i, 'id': i} for i in collection.temp.columns]
                toast = {
                    'children': f'{name} is successfully added.',
                    'is_open': True,
                    'icon': 'success',
                    'header': 'SUCCESS'
                }
                return data, columns, toast
            except Exception as e:
                print('error', e)
                toast = {
                    'children': 'Something wrong with operand. Please choose column with number only',
                    'is_open': True,
                    'icon': 'danger',
                    'header': 'DANGER'
                }
                return  dash.no_update, dash.no_update, toast
        raise  PreventUpdate
#############################################################################################################################################


def register_update_operand_type(app):
    @app.callback(
        [
            Output('operand-icon-0', 'className'),
            Output('operand-icon-1', 'className'),
            Output('operand-icon-2', 'className'),
            Output("operand-type", "data"),
            Output('operand-container-0', 'children'),
            Output('operand-container-1', 'children'),
            Output('operand-container-2', 'children'),
        ],
        [
            Input("operand-icon-0", "n_clicks"),
            Input("operand-icon-1", "n_clicks"),
            Input("operand-icon-2", "n_clicks"),
        ],
        [
            State('operand-icon-0', 'className'),
            State('operand-icon-1', 'className'),
            State('operand-icon-2', 'className'),
            State("operand-type", "data"),

        ],
        prevent_initial_call=True
    )
    def update_operand_type (click0, click1, click2, class0, class1, class2, type):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
            input_value = None
        else:
            input_type = get_ctx_type(ctx)
            input_value = get_ctx_value(ctx)
        if input_type =="operand-icon-0":
            type['0'], class0, child0 = toggle_operand_type(type['0'],0)
            return class0, dash.no_update, dash.no_update, type, child0, dash.no_update, dash.no_update

        elif input_type == "operand-icon-1":
            type['1'], class1, child1 = toggle_operand_type(type['1'],1)
            return dash.no_update, class1, dash.no_update, type, dash.no_update, child1, dash.no_update


        elif input_type == "operand-icon-2":
            type['2'], class2, child2 = toggle_operand_type(type['2'],2)
            return dash.no_update, dash.no_update, class2, type, dash.no_update, dash.no_update, child2

        raise PreventUpdate

#############################################################################################################################################


def register_toggle_new_column_btn(app):
    @app.callback(
        Output('confirm-new-col', 'disabled') ,
        Input("new-column-name", "value"),
        prevent_initial_call=True
    )
    def toggle_new_column_btn (value):
        return True if value == '' else False

#############################################################################################################################################


def register_clear_popup_value(app):
    @app.callback(
        [
            Output('new-column-name', 'value'),
            Output('operator-0', 'value') ,
            Output('operator-1', 'value'),
            Output('operator-2', 'value'),
            Output('operand-0', 'value'),
            Output('operand-1', 'value'),
            Output('operand-2', 'value'),

        ],
        [
            Input("confirm-new-col", "n_clicks"),
            Input("reset-new-col", "n_clicks"),
            Input("exp-undo-0", "n_clicks"),
            Input("exp-undo-1", "n_clicks"),
            Input("exp-undo-2", "n_clicks"),

        ],
        prevent_initial_call=True
    )
    def clear_popup_value (confirm, reset, undo0, undo1, undo2):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
            # input_value = None
        else:
            input_type = get_ctx_type(ctx)
            # input_value = get_ctx_value(ctx)
        # result = {
        #     'name': dash.no_update,
        #     'op0': dash.no_update,
        #     'op1': dash.no_update,
        #     'op2': dash.no_update,
        #     'or0': dash.no_update,
        #     'or1': dash.no_update,
        #     'or2': dash.no_update,
        # }
        if input_type == "confirm-new-col" or input_type == "reset-new-col":
            return '', None, None, None, None, None, None
        elif input_type == "exp-undo-0" :
            return dash.no_update, None, dash.no_update, dash.no_update, None, dash.no_update, dash.no_update
        elif input_type == "exp-undo-1" :
            return dash.no_update, dash.no_update, None,  dash.no_update, dash.no_update, None, dash.no_update
        elif input_type == "exp-undo-2" :
            return dash.no_update, dash.no_update, dash.no_update, None, dash.no_update, dash.no_update, None
        raise  PreventUpdate

#############################################################################################################################################


def register_close_popup(app):
    @app.callback(
        Output('create-new-col-popup', 'is_open') ,
        [
            Input("confirm-new-col", "n_clicks"),
            # Input("create-visual", "n_clicks"),
            # Input("cancel-create-visual", "n_clicks"),

        ],

        prevent_initial_call=True
    )
    def toggle_new_column_btn (confirm):
        if confirm:
            return False
        raise PreventUpdate
#############################################################################################################################################

def register_update_visual_dropdown(app):
    @app.callback(
        Output('visual-type', 'value') ,
        [
            Input("portal-datatable", "columns"),
            # Input("create-visual", "n_clicks"),
            # Input("cancel-create-visual", "n_clicks"),

        ],

        prevent_initial_call=True
    )
    def update_visual_dropdown (col):
        return None

