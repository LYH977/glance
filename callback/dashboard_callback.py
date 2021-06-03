from dash.dependencies import Input, Output

import dash
from dash.exceptions import PreventUpdate

# update play button label according to playing status
from utils.method import get_ctx_type


def register_update_dashboard(app):
    @app.callback(
        [
            Output('landing-scene', 'style'),
            Output('glance-nav', 'className'),
        ],
        [Input('visual-collection', 'children')],
        prevent_initial_call=True
    )
    def update_dashboard(children):


        if len(children) >0:
            return {'opacity':0}, 'black-navbar'
        else:
            return {'opacity':1}, 'transparent-navbar'