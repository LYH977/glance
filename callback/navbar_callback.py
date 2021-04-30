import dash
from dash.dependencies import Input, Output, ALL, State, MATCH
from dash.exceptions import PreventUpdate
import time
import task
from components import container
from components.carousel import create_ca_img
from utils import collection
from utils.method import get_ctx_type, get_ctx_index, formatted_time_value, remove_from_collection
from utils.constant import CAROUSEL, FRAME, TIME, CAROUSEL_CONSTANT, ITEM



# update play button label according to playing status

def register_update_adjust_btn_color(app):
    @app.callback(
        [
            Output('adjust-wrapper', 'style'),
            Output('adjust-svg', 'style'),
        ],
        Input('is-adjusting', 'data'),
        prevent_initial_call=True
    )
    def update_adjust_btn_color(status):
        if status is True:
            wrapper_style = {'background':'#96c3ff'}
            svg_style = {'color':'#196fe3'}
        else:
            wrapper_style = {'background': 'rgb(80, 80, 80)'}
            svg_style = {'color': 'white'}
        return wrapper_style, svg_style



#############################################################################################################################################
def register_toggle_is_adjusting_status(app):
    @app.callback(
        Output('is-adjusting', 'data'),
        Input('adjust-button', 'n_clicks'),
        State('is-adjusting', 'data'),
        prevent_initial_call=True
    )
    def toggle_is_adjusting_status(click, status):
        return True if status is False else False