import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from components import visualization, upload_modal, container
from utils import collection
from utils.method import  get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE




# update visualization container by appending or removing item from array
def register_update_visual_container(app):
    @app.callback(
         Output('visual-container', 'children') ,
        [ Input('create', 'n_clicks'), Input({'type':'dlt-btn', 'index': ALL},'n_clicks') ],
        [ State('visual-container', 'children') , State('parameter', 'data'), State('visual-type', 'value')   ],
        prevent_initial_call=True)
    def update_visual_container(create_clicks, deletable, div_children, param, vtype):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type =get_ctx_type(ctx)
            # input_type = get_ctx_type(ctx)

        if input_type == 'create': # input from add button
            new_child = container.render_container(create_clicks, param, vtype)
            div_children.append(new_child)

            return div_children
        else: # input from delete button
            delete_index = get_ctx_index(ctx)
            del div_children[int(delete_index) -1]
            return div_children


#############################################################################################################################################


# update  figure according to slider
def register_update_figure(app):
    @app.callback(
        Output({'type':'visualization', 'index': MATCH}, 'figure') ,
        [Input({'type':'anim-slider', 'index': MATCH}, 'value')],
        [State({'type':'visualization', 'index': MATCH}, 'figure'),State({'type':'figure-type', 'index': MATCH}, 'data') ],
        prevent_initial_call = True)
    def update_figure(value, fig, ftype):
        fig2 = fig
        # the code below is not necessary
        # fig2['layout']['sliders'][0]['active'] = value
        if ftype == SCATTER_MAP:
            fig2['data'][0] = fig2['frames'][value]['data'][0]
        elif ftype== SCATTER_GEO:
            fig2['data'] = fig2['frames'][value]['data']
        elif ftype == BAR_CHART_RACE:
            fig2['data'][0] = fig2['frames'][value]['data'][0]
        elif ftype == DENSITY:
            fig2['data'][0] = fig2['frames'][value]['data'][0]
        elif ftype == CHOROPLETH:
            fig2['data'][0] = fig2['frames'][value]['data'][0]
        return fig2

#############################################################################################################################################


# update slider according to interval
def register_update_slider(app):
    @app.callback(
        Output({'type':'anim-slider', 'index': MATCH}, 'value'),
        [Input({'type':'interval', 'index': MATCH}, 'n_intervals')],
        State({'type':'is-animating', 'index': MATCH}, 'data')
    )
    def update_slider(value,animate):
        return value if animate is True else dash.no_update

#############################################################################################################################################

# update play button label according to playing status
def register_update_play_btn(app):
    @app.callback(
        [Output({'type':'play-btn', 'index': MATCH}, 'children'), Output({'type':'interval', 'index': MATCH}, 'disabled')],
        [Input({'type':'is-animating', 'index': MATCH}, 'data')],
        prevent_initial_call=True
    )
    def update_play_btn(playing):
        if playing is True:
            return 'pause', False
        else:
            return 'play', True

#############################################################################################################################################

# update playing status according to button click
def register_update_playing_status(app):
    @app.callback(
        [Output({'type':'is-animating', 'index': MATCH}, 'data'), Output({'type':'interval', 'index': MATCH}, 'n_intervals'), Output({'type':'slider-label', 'index': MATCH}, 'children')],
        [Input({'type':'play-btn', 'index': MATCH}, 'n_clicks'), Input({'type':'anim-slider', 'index': MATCH}, 'value')],
        [State({'type':'is-animating', 'index': MATCH}, 'data'), State({'type':'interval', 'index': MATCH}, 'n_intervals'), State({'type':'my_param', 'index': MATCH}, 'data')],
        prevent_initial_call=True
    )
    def update_playing_status(play_clicked, s_value, playing, interval,param):
        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index=get_ctx_index(ctx)

        df_date = collection.data[input_index][param['frame']].unique()
        maxValue = df_date.shape[0] - 1
        if input_type== 'anim-slider': #input from slider

            return \
                False if playing is True and s_value != interval or s_value == maxValue else dash.no_update,\
                dash.no_update, \
                df_date[s_value]

        elif  input_type== 'play-btn':#input from play btn
            return \
                not playing, \
                s_value if s_value != maxValue else 0, \
                dash.no_update

        else:
            raise PreventUpdate




