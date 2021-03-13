
from datetime import datetime, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

import task
from components import visualization, select_dataset_modal, container
from components.visualization import create_figure
from utils import collection
from utils.collection import visual_container
from utils.method import get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index, formatted_time_value, \
    to_nanosecond_epoch, select_query, get_last_timestamp
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    STANDARD_T_FORMAT, FRAME, TIME


# update play button label according to playing status
def register_update_dashboard(app):
    @app.callback(
        Output('empty-scene', 'children'),
        [Input('visual-container', 'children')],
        prevent_initial_call=True
    )
    def update_dashboard(children):
        if len(children) >0:
            return None
        else:
            return 'it is empty'