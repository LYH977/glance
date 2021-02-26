import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from components import visualization, upload_modal, container
from utils import collection
from utils.method import  get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, FRAME_NAME



def register_display_image(app):
    @app.callback(Output({'type':'fade1', 'index': MATCH}, 'children'),
                   # Output({'type':'fade2', 'index': MATCH}, 'children')
                   # ,Output('fade1', 'style'),Output('fade2', 'style')

                  [Input({'type':'ca-anim-slider', 'index': MATCH}, 'value')],
                  prevent_initial_call=True
                  )
    def display_image(value):

        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        # print(collection.data[input_index].loc[value,'link'])
        # print(interval, 'inside 1')
        # img = html.Img(src="http://placeimg.com/625/225/arch")
        # img = image[interval]
        imgsrc =  collection.data[input_index].loc[value,'link']
        img = html.Img(src=imgsrc, style={ 'height':300, 'width':300 })
        # img = html.Img(src="https://firebasestorage.googleapis.com/v0/b/glance-4685b.appspot.com/o/images%2Ftest.jpg?alt=media")
        return img
        # , {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}


        # ,{'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}

        # else:
        #     raise PreventUpdate


# update slider according to interval
def register_ca_update_slider(app):
    @app.callback(
        Output({'type':'ca-anim-slider', 'index': MATCH}, 'value'),
        [Input({'type':'ca-interval', 'index': MATCH}, 'n_intervals')],
        State({'type':'ca-is-animating', 'index': MATCH}, 'data')
    )
    def update_ca_slider(value,animate):
        return value if animate is True else dash.no_update

#############################################################################################################################################

# update play button label according to playing status
def register_update_ca_play_btn(app):
    @app.callback(
        [Output({'type':'ca-play-btn', 'index': MATCH}, 'children'), Output({'type':'ca-interval', 'index': MATCH}, 'disabled')],
        [Input({'type':'ca-is-animating', 'index': MATCH}, 'data')],
        prevent_initial_call=True
    )
    def update_ca_play_btn(playing):
        if playing is True:
            return 'pause', False
        else:
            return 'play', True
#############################################################################################################################################

# update playing status according to button click
def register_update_ca_playing_status(app):
    @app.callback(
        [Output({'type':'ca-is-animating', 'index': MATCH}, 'data'), Output({'type':'ca-interval', 'index': MATCH}, 'n_intervals'), Output({'type':'ca-slider-label', 'index': MATCH}, 'children')],
        [Input({'type':'ca-play-btn', 'index': MATCH}, 'n_clicks'), Input({'type':'ca-anim-slider', 'index': MATCH}, 'value')],
        [State({'type':'ca-is-animating', 'index': MATCH}, 'data'), State({'type':'ca-interval', 'index': MATCH}, 'n_intervals'), State({'type':'ca-my_param', 'index': MATCH}, 'data')],
        prevent_initial_call=True
    )
    def update_ca_playing_status(play_clicked, s_value, playing, interval, param):
        # print(collection.data)
        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        df_date = collection.data[input_index][param[FRAME_NAME[CAROUSEL]]].unique()
        maxValue = df_date.shape[0] - 1
        if input_type== 'ca-anim-slider': #input from slider

            return \
                False if playing is True and s_value != interval or s_value == maxValue else dash.no_update,\
                dash.no_update, \
                df_date[s_value]

        elif  input_type== 'ca-play-btn':#input from play btn
            return \
                not playing, \
                s_value if s_value != maxValue else 0, \
                dash.no_update

        else:
            raise PreventUpdate

