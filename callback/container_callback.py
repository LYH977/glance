import json
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

import task
from components import visualization, select_dataset_modal, container
from components.carousel import create_ca_img
from components.visualization import create_figure, collapse_markup
from utils import collection
from utils.collection import visual_container, redis_instance
from utils.method import get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index, formatted_time_value, \
    to_nanosecond_epoch, select_query, get_last_timestamp
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    STANDARD_T_FORMAT, FRAME, TIME, MAXIMUM, MINIMUM, CAROUSEL_CONSTANT, ITEM


# update visualization container by appending or removing item from array
def register_update_visual_container(app):
    @app.callback(
         Output('visual-container', 'children') ,
        [ Input('create-visual', 'n_clicks'), Input({'type':'dlt-btn', 'index': ALL},'n_clicks') ],
        [ State('visual-container', 'children') , State('last-param', 'data'),  State('chosen-tformat', 'data')    ],
        prevent_initial_call=True)
    def update_visual_container(create_clicks, deletable, div_children, param, tformat):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        if input_type == 'create-visual': # input from add button
            collection.temp = collection.temp.dropna()
            collection.temp.reset_index(drop=True, inplace=True)
            collection.temp[FRAME] = collection.temp[TIME].map(lambda x: formatted_time_value(x, tformat))
            collection.data[create_clicks] = collection.temp
            collection.live_processing[create_clicks] = False

            if param['vtype'] != CAROUSEL: #  carousel
                temp = []
                for row in collection.temp.index:
                    temp.append( create_ca_img(collection.temp.loc[row, param['parameter'][CAROUSEL_CONSTANT[ITEM]]]) )
                collection.img_container[input_index] = temp
            else: # other than carousel
                # task.process_dataset(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'])
                result = task.process_dataset.delay(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'])
            new_child = container.render_container(create_clicks, param['parameter'], param['vtype'], tformat)
            div_children.append(new_child)
            visual_container.append(create_clicks)
            return div_children

        else: # input from delete button
            print('visual_container:', visual_container)
            # delete_index = get_ctx_index(ctx)
            temp = visual_container.index(input_index)
            del div_children[temp]
            del visual_container[temp]
            return div_children


#############################################################################################################################################