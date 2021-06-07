import dash
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

from components.carousel import create_ca_img
from utils import collection
from utils.export.export_data import export_img_mp4
from utils.method import get_ctx_type, get_ctx_index, formatted_time_value, \
    select_query, get_last_timestamp
from utils.constant import FRAME, TIME, CAROUSEL_CONSTANT, ITEM
from datetime import datetime


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
        # [
            Output({'type':'ca-is-animating', 'index': MATCH}, 'data'),
            # Output({'type':'ca-interval', 'index': MATCH}, 'n_intervals'),
            # Output({'type':'ca-slider-label', 'index': MATCH}, 'children')
        # ],
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
            return False if playing is True and s_value != interval or s_value == maxValue else dash.no_update
                # df_date[s_value]
        elif  input_type== 'ca-play-btn':#input from play btn
            return not playing
                # dash.no_update
        elif  input_type== 'ca-live-mode':#input from play btn
            return False if live is True else dash.no_update
                # dash.no_update
        else:
            raise PreventUpdate
#############################################################################################################################################

def register_reset_ca_slider_n_interval(app):
    @app.callback(
        Output({'type': 'ca-interval', 'index': MATCH}, 'n_intervals'),
        Input({'type': 'ca-play-btn', 'index': MATCH}, 'n_clicks'),
        State({'type': 'ca-anim-slider', 'index': MATCH}, 'value'),

        prevent_initial_call=True
    )
    def reset_slider_n_interval(play, slider):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        df_date = collection.data[input_index][FRAME].unique()
        maxValue = df_date.shape[0] - 1
        return slider if slider != maxValue else 0
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
        Output({'type':'ca-last-timestamp', 'index': MATCH}, 'data'),
        [Input({'type':'ca-live-interval', 'index': MATCH}, 'n_intervals')],
        [
            State({'type':'ca-last-timestamp', 'index': MATCH}, 'data'),
            State({'type':'frame-format', 'index': MATCH}, 'data'),
            State({'type': 'my_param', 'index': MATCH}, 'data'),
            State({'type': 'db-name', 'index': MATCH}, 'data')

        ],
        prevent_initial_call=True
    )
    def update_live_data(live, ts, format,  param, dbname):
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
            result = select_query(dbname, ' where time >{}'.format(ts))

            if result is not None:
                result[TIME] = result.index.map(lambda x: str(x).split('+')[0])
                result[FRAME] = result[TIME].map(lambda x: formatted_time_value(x, format))
                last_nano = get_last_timestamp(result[TIME])
                collection.data[input_index] = collection.data[input_index].append(result, ignore_index=True)


                for row in result.index:
                    collection.img_container[input_index].append(
                        create_ca_img(
                            result.loc[row, param['parameter'][CAROUSEL_CONSTANT[ITEM]]],
                            result.loc[row, FRAME],

                        )
                    )

                # fig = create_figure(collection.data[input_index], param, ftype)
                return last_nano

            else:
                collection.live_processing[input_index] = False
                raise PreventUpdate

#############################################################################################################################################

#############################################################################################################################################

def register_export_ca_visual(app):
    @app.callback(
        [
            Output({'type': 'ca-download-btn', 'index': MATCH}, 'download'),
            Output({'type': 'ca-download-btn', 'index': MATCH}, 'href'),
            Output({'type': 'ca-download-btn-wrapper', 'index': MATCH}, 'style'),
            Output({'type': 'ca-generate-btn', 'index': MATCH}, 'hidden'),
        ],
        [Input({'type': 'ca-generate-btn', 'index': MATCH}, 'disabled')],
        [
            State({'type': 'ca-export-name', 'index': MATCH}, 'data'),
        ],
        prevent_initial_call=True
    )
    def export_ca_visual(disabled, name):
        if disabled:
            ctx = dash.callback_context
            input_index = get_ctx_index(ctx)
            export_img_mp4(input_index, name)
            dl = f'{name}.mp4'
            path = app.get_asset_url(f'export/{dl}')
            print(f'habis href {name}')
            return dl, path, {'display': 'block'}, True
        return None, None, {'display': 'none'}, False


# ############################################################################################################################################

def register_ca_handle_export_btn_click(app):
    @app.callback(
        [
            Output({'type': 'ca-generate-btn', 'index': MATCH}, 'disabled'),
            Output({'type': 'ca-export-name', 'index': MATCH}, 'data'),
        ],
        [
            Input({'type': 'ca-generate-btn', 'index': MATCH}, 'n_clicks'),
            Input({'type': 'ca-regenerate-btn', 'index': MATCH}, 'n_clicks'),
        ],
        [
            State({'type': 'ca-generate-btn', 'index': MATCH}, 'disabled'),
        ],
        prevent_initial_call=True
    )
    def handle_ca_export_btn_click(btn_click, enable,   disabled):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)
        if input_type== 'ca-generate-btn' and btn_click and not disabled:
            now = int(datetime.now().timestamp())
            return  True, now
        elif input_type =='ca-regenerate-btn' and enable :
            return False,  dash.no_update

        raise PreventUpdate


# ############################################################################################################################################

def register_ca_reset_export_interval(app):
    @app.callback(
        Output({'type': 'ca-export-interval', 'index': MATCH}, 'n_intervals'),
        [Input({'type': 'ca-generate-btn', 'index': MATCH}, 'n_clicks')],
        prevent_initial_call=True
    )
    def reset_export_interval(click):
        return 0


# ############################################################################################################################################

def register_ca_update_generate_btn_name(app):
    @app.callback(
        [
            Output({'type': 'ca-generate-btn', 'index': MATCH}, 'children'),
            Output({'type': 'ca-export-interval', 'index': MATCH}, 'disabled'),
        ],
        [
            Input({'type': 'ca-export-interval', 'index': MATCH}, 'n_intervals'),
            Input({'type': 'ca-generate-btn', 'index': MATCH}, 'disabled'),
        ],
        prevent_initial_call=True
    )
    def update_generate_btn_name(interval, disabled):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)
        input_index = get_ctx_index(ctx)
        if input_type == 'ca-export-interval':
            estimate = len(collection.data[input_index])
            # estimate = 3+1
            result = estimate - interval
            if result > 0:
                name = f'Ready in {result}s'
                itv = dash.no_update
            else:
                name =  'Ready soon'
                itv = True
            return name, itv

        elif input_type == 'ca-generate-btn' :
            if disabled:
                return 'Generating...', False
            else:
                return 'Generate MP4', dash.no_update
        raise  PreventUpdate


def register_ca_toggle_enable_btn(app):
    @app.callback(

        Output({'type': 'ca-regenerate-btn', 'index': MATCH}, 'style'),
        Input({'type': 'ca-download-btn', 'index': MATCH}, 'download'),

        prevent_initial_call=True
    )
    def toggle_enable_btn(data):
        return {'display':'block'}  if data is not None else  {'display':'none'}