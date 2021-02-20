import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from components import visualization, upload_modal, container
from utils import collection
from utils.method import  set_slider_calendar

import os
import base64



# update visualization container by appending or removing item from array
def register_update_visual_container(app):
    @app.callback(
         Output('visual-container', 'children') ,
        [ Input('create', 'n_clicks'), Input({'type':'dlt-btn', 'index': ALL},'n_clicks') ],
        [ State('visual-container', 'children') , State('parameter', 'data')  ],
        prevent_initial_call=True)
    def update_visual_container(add_clicks, deletable, div_children, param):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if input_id == 'create': # input from add button
            uuid = base64.b64encode(os.urandom(6)).decode('ascii')
            new_child = container.render_container(add_clicks, param,uuid)

            div_children.append(new_child)
            return div_children
        else: # input from delete button
            delete_index = input_id.split(',')[0].split(':')[1]
            del div_children[int(delete_index) -1]
            return div_children



# update  figure according to slider
def register_update_figure(app):
    @app.callback(
        [Output({'type':'visualization', 'index': MATCH}, 'figure') ],
        [Input('anim-slider', 'value')],
        [State({'type':'visualization', 'index': MATCH}, 'figure')],
        prevent_initial_call = True)
    def update_figure(value, fig):
        fig2 = fig
        # the code below is not necessary
        # fig2['layout']['sliders'][0]['active'] = value
        fig2['data'][0] = fig2['frames'][value]['data'][0]
        return [fig2]



# update slider according to interval
def register_update_slider(app):
    @app.callback(
        Output('anim-slider', 'value'),
        [Input('interval', 'n_intervals')],
        State('is-animating', 'data')
    )
    def update_slider(value,animate):
        return value if animate is True else dash.no_update


# update play button label according to playing status
def register_update_play_btn(app):
    @app.callback(
        [Output('play-btn', 'children'), Output('interval', 'disabled')],
        [Input('is-animating', 'data')],
        prevent_initial_call=True
    )
    def update_play_btn(playing):
        if playing is True:
            return 'pause', False
        else:
            return 'play', True


# update playing status according to button click
def register_update_playing_status(app):
    @app.callback(
        [Output('is-animating', 'data'), Output('interval', 'n_intervals'), Output('slider-label', 'children')],
        [Input('play-btn', 'n_clicks'), Input('anim-slider', 'value')],
        [State('is-animating', 'data'), State('interval', 'n_intervals')],
        prevent_initial_call=True
    )
    def update_playing_status(play_clicked, s_value, playing, interval):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_id = 'No input yet'
        else:
            input_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if input_id== 'anim-slider': #input from slider
            return \
                False if playing is True and s_value != interval or s_value == visualization.maxValue else dash.no_update,\
                dash.no_update, \
                visualization.df_date[s_value]

        elif  input_id== 'play-btn':#input from play btn
            return \
                not playing, \
                s_value if s_value != visualization.maxValue else 0, \
                dash.no_update

        else:
            raise PreventUpdate




