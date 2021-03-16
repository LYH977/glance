import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from components import visualization, select_dataset_modal, container
from utils import collection
from utils.method import  get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, FRAME


def register_display_image(app):
    @app.callback(Output({'type':'fade1', 'index': MATCH}, 'children'),
                  [Input({'type':'ca-anim-slider', 'index': MATCH}, 'value')],
                  [
                      State({'type': 'ca-at-max', 'index': MATCH}, 'data'),
                      State({'type': 'ca-live-mode', 'index': MATCH}, 'on'),
                  ],
                  prevent_initial_call=True
                  )
    def display_image(value, atmax, live):

        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
            raise PreventUpdate
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        val = value
        if live and atmax:
            new_max = len(collection.img_container[input_index])
            val = new_max - 1
        imgsrc =  collection.img_container[input_index][val]
        # img = html.Img(src=imgsrc, style={ 'height':300, 'width':300 })
        # img = html.Img(src="https://firebasestorage.googleapis.com/v0/b/glance-4685b.appspot.com/o/images%2Ftest.jpg?alt=media")
        return imgsrc

#############################################################################################################################################


# update slider according to interval
# def register_ca_update_slider(app):
#     @app.callback(
#         Output({'type':'ca-anim-slider', 'index': MATCH}, 'value'),
#         [Input({'type':'ca-interval', 'index': MATCH}, 'n_intervals')],
#         State({'type':'ca-is-animating', 'index': MATCH}, 'data')
#     )
#     def update_ca_slider(value,animate):
#         return value if animate is True else dash.no_update

def register_ca_update_slider(app):
    @app.callback(
        [
            Output({'type':'ca-anim-slider', 'index': MATCH}, 'value'),
            Output({'type': 'ca-anim-slider', 'index': MATCH}, 'max'),
            Output({'type': 'ca-interval', 'index': MATCH}, 'max_intervals')
        ],
        [
            Input({'type':'ca-interval', 'index': MATCH}, 'n_intervals'),
            Input({'type': 'ca-last-timestamp', 'index': MATCH}, 'data')
        ],
        [
            State({'type':'ca-is-animating', 'index': MATCH}, 'data'),
            State({'type': 'ca-at-max', 'index': MATCH}, 'data'),
        ],
        prevent_initial_call=True
    )
    def update_ca_slider(value, ts, animate, atmax):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        if input_type == 'ca-interval':
            if animate is True:
                return value, dash.no_update, dash.no_update
            else:
                raise PreventUpdate
        elif input_type == 'ca-last-timestamp':
            df_frame = collection.data[input_index][FRAME].unique()
            maxValue = df_frame.shape[0] - 1
            collection.live_processing[input_index] = False
            return maxValue if atmax else dash.no_update, maxValue, maxValue

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
        [
            Output({'type':'ca-is-animating', 'index': MATCH}, 'data'),
            Output({'type':'ca-interval', 'index': MATCH}, 'n_intervals'),
            Output({'type':'ca-slider-label', 'index': MATCH}, 'children')
        ],
        [
            Input({'type':'ca-play-btn', 'index': MATCH}, 'n_clicks'),
            Input({'type':'ca-anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'ca-live-mode', 'index': MATCH}, 'on')
        ],
        [
            State({'type':'ca-is-animating', 'index': MATCH}, 'data'),
            State({'type':'ca-interval', 'index': MATCH}, 'n_intervals'),
        ],
        prevent_initial_call=True
    )
    def update_ca_playing_status(play_clicked, s_value, live, playing, interval):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        df_date = collection.data[input_index][FRAME].unique()
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
        elif  input_type== 'ca-live-mode':#input from play btn
            return \
                False if live is True else dash.no_update , \
                dash.no_update, \
                dash.no_update
        else:
            raise PreventUpdate

#############################################################################################################################################

# update live interval according to live switch
def register_update_ca_live_mode(app):
    @app.callback(
       [ Output({'type':'ca-live-interval', 'index': MATCH}, 'disabled'), Output({'type':'ca-play-btn', 'index': MATCH}, 'disabled')],
        [Input({'type':'ca-live-mode', 'index': MATCH}, 'on')],
        prevent_initial_call=True
    )
    def update_live_mode(live):
        return not live, live

#############################################################################################################################################

# update live interval according to live switch
def register_ca_update_atmax(app):
    @app.callback(
        Output({'type': 'ca-at-max', 'index': MATCH}, 'data'),
        [Input({'type':'ca-anim-slider', 'index': MATCH}, 'value'),],
        State({'type': 'ca-anim-slider', 'index': MATCH}, 'max'),

        prevent_initial_call=True
    )
    def update_atmax(slider, smax):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        return True if slider == smax else False

#############################################################################################################################################

# fetch new data for live mode
def register_ca_update_live_data(app):
    @app.callback(
        [Output({'type':'ca-last-timestamp', 'index': MATCH}, 'data'),Output({'type':'back-buffer', 'index': MATCH}, 'data')],
        [Input({'type':'ca-live-interval', 'index': MATCH}, 'n_intervals')],
        [
            State({'type':'ca-last-timestamp', 'index': MATCH}, 'data'),
            State({'type':'ca-frame-format', 'index': MATCH}, 'data'),
            State({'type': 'ca-my_param', 'index': MATCH}, 'data')
        ],
        prevent_initial_call=True
    )
    def update_live_data(live, ts, format,  param):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        if collection.live_processing[input_index] is True:
            raise  PreventUpdate
        else:
            collection.live_processing[input_index] = True
            result = select_query('live', ' where time >{}'.format(ts))

            if result is not None:
                result[TIME] = result.index.map(lambda x: str(x).split('+')[0])
                result[FRAME] = result[TIME].map(lambda x: formatted_time_value(x, format))
                # result.reset_index(drop=True, inplace=True)
                last_nano = get_last_timestamp(result[TIME])
                collection.data[input_index] = collection.data[input_index].append(result, ignore_index=True)
                fig = create_figure(collection.data[input_index], param, ftype)
                print('last_nano',last_nano)
                return last_nano,fig

            else:
                collection.live_processing[input_index] = False
                raise PreventUpdate