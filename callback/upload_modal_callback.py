import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash
from dash.exceptions import PreventUpdate

from components.carousel import create_ca_img
from utils.constant import FIGURE_OPTION, SCATTER_MAP_PARAM, SM_PARAM, CA_PARAM, CH_PARAM, D_PARAM, BC_PARAM, SG_PARAM, \
    CAROUSEL, CAROUSEL_CONSTANT, ITEM
from utils import collection
from utils.method import get_ctx_type,get_ctx_property,get_ctx_value,get_ctx_index
from components.upload_modal import output_form_markup,after_upload_markup, after_upload_markup
import base64
import io
import json
import pandas as pd





def validate_create(data):
    ctx = dash.callback_context
    input_value = None
    if not ctx.triggered:
        input_id = 'No input yet'
        raise PreventUpdate
    else:
        input_type = get_ctx_type(ctx)
        input_value = get_ctx_value(ctx)
    data['parameter'][input_type] = input_value
    is_filled = False if None in data['parameter'].values() else True
    # print(data['parameter'])
    return {'is_filled': is_filled, 'parameter': data['parameter']}

#############################################################################################################################################

def parse_contents(contents, filename, date):
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
    return after_upload_markup(filename)

#############################################################################################################################################

# def register_update_option(app):
#     @app.callback( [ Output("parameter", "data"), Output('is-filled', 'data')],
#                 [
#                     # Input("latitude", "value"),
#                     # Input("longitude", "value"),
#                     # Input("size", "value"),
#                     Input("color", "value"),
#                     Input("name", "value"),
#                     Input("frame", "value"),
#                     Input("message", "value"),
#                     # Input("item", "value"),
#                     # Input("value", "value"),
#                     # Input("z", "value"),
#                     Input("locations", "value"),
#                     Input('visual-type','value')
#                 ],
#                     State("parameter", "data"),
#                     prevent_initial_call=True
#     )
#     def update_option(
#             # lat, long,size
#              color, name,
#             frame,msg, locations,
#             # msg,item,value
#              visual, param):
#         ctx = dash.callback_context
#         input_value = None
#         if not ctx.triggered:
#             input_id = 'No input yet'
#             raise PreventUpdate
#         else:
#             input_type = get_ctx_type(ctx)
#             input_value = get_ctx_value(ctx)
#
#
#         param[input_type] = input_value
#         is_filled = False if None in param.values() or visual is None else True
#         # print(param)
#         return  param, is_filled


#############################################################################################################################################


def register_update_after_upload(app):
    @app.callback(Output('after-upload', 'children'),
                  [Input("open", "n_clicks"), Input("close", "n_clicks"),Input("create", "n_clicks"), Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'), State('upload-data', 'last_modified'),State("modal", "is_open")],
                  prevent_initial_call=True
    )
    def update_after_upload(n1, n2,n3,list_of_contents, list_of_names, list_of_dates,is_open):
        ctx = dash.callback_context
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
                  Input("visual-type", "value"),
                  prevent_initial_call=True
    )
    def update_output_form(type):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_id == 'visual-type' and type is not None:
            return output_form_markup(type)
        # elif input_id == 'close' or input_id == 'create':
        #     return None
        else:
            raise PreventUpdate

#############################################################################################################################################


def register_toggle_modal(app):
    @app.callback(
        Output("modal", "is_open"),
        [Input("open", "n_clicks"), Input("close", "n_clicks"),Input("create", "n_clicks")],
        [State("modal", "is_open"), State('last-param', 'data')],
        prevent_initial_call=True
    )
    def toggle_modal (open, close, create, is_open, param):
        print(param)
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if input_id == 'create':
            collection.data[create] = collection.temp.dropna()
            # collection.last_create_click = create
            if param['vtype'] == CAROUSEL:
                temp = []
                for row in collection.temp.index:
                    temp.append( create_ca_img(collection.temp.loc[row, param['parameter'][CAROUSEL_CONSTANT[ITEM]]]) )
                collection.img_container[create] = temp
            # print(collection.data[create]['year'])
        return not is_open
#############################################################################################################################################


def register_enable_create_btn(app):
    @app.callback(
        [Output('create', 'disabled'),  Output('last-param', 'data')] ,
        [
            Input(SM_PARAM,'data'),
            Input(SG_PARAM, 'data'),
            Input(D_PARAM, 'data'),
            Input(CH_PARAM, 'data'),
            Input(CA_PARAM, 'data'),
            Input(BC_PARAM, 'data'),
            Input('create', 'n_clicks'),
        ],
        State('visual-type', 'value'),
        prevent_initial_call=True
    )
    def enable_create_btn (sm, sg, d, ch, ca, bc, create, vtype):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
            input_value=None
        else:
            input_id = get_ctx_type(ctx)
            input_value = get_ctx_value(ctx)

        if input_id == 'create':
            return True, dash.no_update
        if input_value['parameter'] is not None and input_value['is_filled'] is True:
            data = {'vtype': vtype, 'parameter':input_value['parameter'] }
            return False, data
        else:
            raise PreventUpdate
#############################################################################################################################################


def register_clear_upload(app):
    @app.callback(
        Output('upload-data', 'contents') ,
        [Input('close','n_clicks'), Input('create','n_clicks')],
        prevent_initial_call=True
    )
    def clear_upload (close,create):
        return None

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
            Input("sm_frame", "value"),
            Input("sm_message", "value"),
        ],
        State(SM_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_sm_create (lat, long, size, color, name, frame, msg, data):
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
            Input("sg_frame", "value"),
            Input("sg_message", "value"),
        ],
        State(SG_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_sg_create (lat, long, size, color, name, frame, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_bc_create(app):
    @app.callback(
        Output(BC_PARAM, 'data') ,
        [
            Input("bc_item", "value"),
            Input("bc_value", "value"),
            Input("bc_frame", "value"),
        ],
        State(BC_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_bc_create (item, value, frame, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_d_create(app):
    @app.callback(
        Output(D_PARAM, 'data') ,
        [
            Input("d_latitude", "value"),
            Input("d_longitude", "value"),
            Input("d_z", "value"),
            Input("d_frame", "value"),
            Input("d_message", "value"),
        ],
        State(D_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_d_create (lat, long, z, frame, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ch_create(app):
    @app.callback(
        Output(CH_PARAM, 'data') ,
        [
            Input("ch_locations", "value"),
            Input("ch_color", "value"),
            Input("ch_name", "value"),
            Input("ch_frame", "value"),
            Input("ch_message", "value"),
        ],
        State(CH_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ch_create (loc, color, name, frame, msg, data):
        return validate_create(data)


#############################################################################################################################################


def register_validate_ca_create(app):
    @app.callback(
        Output(CA_PARAM, 'data') ,
        [
            Input("ca_item", "value"),
            Input("ca_frame", "value"),
        ],
        State(CA_PARAM, 'data'),
        prevent_initial_call=True
    )
    def validate_ca_create (item, frame, data):
        return validate_create(data)


