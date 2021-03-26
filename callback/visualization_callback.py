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
from components.visualization import create_figure, collapse_markup
from utils import collection
from utils.collection import visual_container, redis_instance
from utils.method import get_ctx_type, get_ctx_property, get_ctx_value, get_ctx_index, formatted_time_value, \
    to_nanosecond_epoch, select_query, get_last_timestamp
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    STANDARD_T_FORMAT, FRAME, TIME, MAXIMUM, MINIMUM, VISUAL_HEIGHT, COLLAPSE_HEIGHT


def change_frame(ftype, fig2, value):
    if ftype == SCATTER_MAP:
        fig2['data'][0] = fig2['frames'][value]['data'][0]
    elif ftype == SCATTER_GEO:
        fig2['data'] = fig2['frames'][value]['data']
    elif ftype == BAR_CHART_RACE:
        fig2['data'][0] = fig2['frames'][value]['data'][0]
    elif ftype == DENSITY:
        fig2['data'][0] = fig2['frames'][value]['data'][0]
    elif ftype == CHOROPLETH:
        fig2['data'][0] = fig2['frames'][value]['data'][0]

def handleOutOfRangeNotif(celery, slider):
    length = len(celery)
    if slider > length - 1:
        return True

def assign_style (toggle):
    if toggle:
        ostyle = {'height': '40%'}
        nstyle = {
            # 'display': 'block',
            'height': '150px'}

    else:
        ostyle = {'height': '15%'}
        nstyle = {
            # 'display': 'hidden',
            'height': 0, }
    return ostyle, nstyle


#############################################################################################################################################


# update  figure according to slider
def register_update_figure(app):
    @app.callback(
        Output({'type': 'visualization', 'index': MATCH}, 'figure'),
        [
            Input({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'legend-theme', 'index': MATCH}, 'on'),
        ],
        [
            State({'type': 'my_param', 'index': MATCH}, 'data'),
            State({'type': 'at-max', 'index': MATCH}, 'data'),
            State({'type': 'live-mode', 'index': MATCH}, 'on'),
            State({'type': 'back-buffer', 'index': MATCH}, 'data'),

        ],
        prevent_initial_call=True)
    def update_figure(value,legend, param, atmax, live, new_fig):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        # fig2 = new_fig
        if input_type == 'anim-slider':
            fig2 = new_fig
            val = value
            if live and atmax:
                new_max = len(new_fig['frames'])
                val = new_max - 1
            change_frame(param['vtype'], fig2, val)
            return fig2
        elif input_type == 'legend-theme':
            fig2 = new_fig
            if legend : #dark theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,0.5)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
            else: # light theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,0.5)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
            change_frame(param['vtype'], fig2, value)
            return fig2
        else:
            raise PreventUpdate

############################################################################################################################################## update slider according to interval
def register_update_slider(app):
    @app.callback(
        [
            Output({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Output({'type': 'anim-slider', 'index': MATCH}, 'max'),
            Output({'type': 'interval', 'index': MATCH}, 'max_intervals')
        ],
        [
            Input({'type': 'interval', 'index': MATCH}, 'n_intervals'),
            Input({'type': 'last-timestamp', 'index': MATCH}, 'data')
        ],
        [
            State({'type': 'is-animating', 'index': MATCH}, 'data'),
            State({'type': 'at-max', 'index': MATCH}, 'data'),
        ],
        prevent_initial_call=True
    )
    def update_slider(value, ts, animate, atmax):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        if input_type == 'interval':
            if animate is True:
                return value, dash.no_update, dash.no_update
            else:
                raise PreventUpdate
        elif input_type == 'last-timestamp':
            df_frame = collection.data[input_index][FRAME].unique()
            maxValue = df_frame.shape[0] - 1
            collection.live_processing[input_index] = False
            return maxValue if atmax else dash.no_update, maxValue, maxValue


#############################################################################################################################################

# update play button label according to playing status

def register_update_play_btn(app):
    @app.callback(
        [Output({'type': 'play-btn', 'index': MATCH}, 'children'),
         Output({'type': 'interval', 'index': MATCH}, 'disabled')],
        [Input({'type': 'is-animating', 'index': MATCH}, 'data')],
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
        [
            Output({'type': 'is-animating', 'index': MATCH}, 'data'),
            Output({'type': 'interval', 'index': MATCH}, 'n_intervals'),
            Output({'type': 'slider-label', 'index': MATCH}, 'children'),
        ],
        [
            Input({'type': 'play-btn', 'index': MATCH}, 'n_clicks'),
            Input({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'live-mode', 'index': MATCH}, 'on')
        ],
        [
            State({'type': 'is-animating', 'index': MATCH}, 'data'),
            State({'type': 'interval', 'index': MATCH}, 'n_intervals'),

        ],
        prevent_initial_call=True
    )
    def update_playing_status(play_clicked, s_value, live, playing, interval):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        # print('param', param)
        df_frame = collection.data[input_index][FRAME].unique()
        maxValue = df_frame.shape[0] - 1
        if input_type == 'anim-slider':  # input from slider
            label = df_frame[s_value]
            return \
                False if playing is True and s_value != interval or s_value == maxValue else dash.no_update, \
                dash.no_update, \
                label

        elif input_type == 'play-btn':  # input from play btn
            return \
                not playing, \
                s_value if s_value != maxValue else 0, \
                dash.no_update
        elif input_type == 'live-mode':  # input from play btn
            return \
                False if live is True else dash.no_update, \
                dash.no_update, \
                dash.no_update
        else:
            raise PreventUpdate


#############################################################################################################################################

# update live interval according to live switch
def register_update_atmax(app):
    @app.callback(
        Output({'type': 'at-max', 'index': MATCH}, 'data'),
        [Input({'type': 'anim-slider', 'index': MATCH}, 'value'), ],
        State({'type': 'anim-slider', 'index': MATCH}, 'max'),

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


# ############################################################################################################################################

# update live interval according to live switch
def register_update_live_mode(app):
    @app.callback(
        [
            Output({'type': 'live-interval', 'index': MATCH}, 'disabled'),
            Output({'type': 'play-btn', 'index': MATCH}, 'disabled'),
        ],
        [Input({'type': 'live-mode', 'index': MATCH}, 'on')],
        prevent_initial_call=True
    )
    def update_live_mode(live):
        return not live, live


#############################################################################################################################################

# fetch new data for live mode
def register_update_live_data(app):
    @app.callback(
        [
            Output({'type': 'last-timestamp', 'index': MATCH}, 'data'),
            Output({'type': 'back-buffer', 'index': MATCH}, 'data'),
        ],
        [
            Input({'type': 'live-interval', 'index': MATCH}, 'n_intervals'),
            Input({'type': 'legend-theme', 'index': MATCH}, 'on'),

        ],
        [
            State({'type': 'last-timestamp', 'index': MATCH}, 'data'),
            State({'type': 'frame-format', 'index': MATCH}, 'data'),
            State({'type': 'my_param', 'index': MATCH}, 'data'),
            State({'type': 'db-name', 'index': MATCH}, 'data'),
            State({'type': 'back-buffer', 'index': MATCH}, 'data'),

        ],
        prevent_initial_call=True
    )
    def update_live_data(live, legend, ts, format,  param, dbname, buffer):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        # print(datetime.now(),' collection.live_processing', collection.live_processing)
        if input_type =='live-interval':
            if collection.live_processing[input_index] is True:
                raise PreventUpdate
            else:
                collection.live_processing[input_index] = True
                result = select_query(dbname, ' where time >{}'.format(ts))

                if result is not None:
                    result[TIME] = result.index.map(lambda x: str(x).split('+')[0])
                    result[FRAME] = result[TIME].map(lambda x: formatted_time_value(x, format))
                    # result.reset_index(drop=True, inplace=True)
                    last_nano = get_last_timestamp(result[TIME])
                    collection.data[input_index] = collection.data[input_index].append(result, ignore_index=True)
                    fig = create_figure(collection.data[input_index], param['parameter'], param['vtype'])
                    # print('last_nano',last_nano)
                    return last_nano, fig

                else:
                    collection.live_processing[input_index] = False
                    raise PreventUpdate
        elif input_type == 'legend-theme':
            fig2 = buffer
            if legend : #dark theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,0.5)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
            else: # light theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,0.5)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
            return dash.no_update,fig2

        raise PreventUpdate


#############################################################################################################################################

# update live interval according to live switch
def register_toggle_collapse(app):
    @app.callback(
        [
            Output({'type': 'last-notif-click', 'index': MATCH}, 'data'),
            Output({'type': 'is-slided-up', 'index': MATCH}, 'data'),
            Output({'type': 'option-wrapper', 'index': MATCH}, 'style'),
            Output({'type': 'notif-body-wrapper', 'index': MATCH}, 'style'),

        ],
        [
            Input({'type': 'celery-data', 'index': MATCH}, 'data'),
            Input({'type': f'{MAXIMUM}-notif', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'{MINIMUM}-notif', 'index': MATCH}, 'n_clicks')
        ],
        [
            State({'type': 'last-notif-click', 'index': MATCH}, 'data'),
            State({'type': 'is-slided-up', 'index': MATCH}, 'data'),

        ],
        prevent_initial_call=True
    )
    def toggle_collapse(celery, max, min, state, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
        if input_type == 'celery-data':
            ostyle, nstyle = assign_style(is_open)
            return dash.no_update, dash.no_update, ostyle, nstyle

        if input_type == f'{MAXIMUM}-notif' and max is not None or input_type == f'{MINIMUM}-notif' and min is not None:
            toggle = False if input_type == state and is_open else True
            ostyle, nstyle = assign_style(toggle)
            return input_type, toggle, ostyle, nstyle

        raise PreventUpdate


#############################################################################################################################################

# update lcelery data according to interval
def register_update_celery_data(app):
    @app.callback(
        [
            Output({'type': 'celery-data', 'index': MATCH}, 'data'),
            Output({'type': 'celery-interval', 'index': MATCH}, 'disabled'),
            Output({'type': 'loading-notif-output', 'index': MATCH}, 'children')
        ],
        [
            Input({'type': 'celery-interval', 'index': MATCH}, 'n_intervals'),
            Input({'type': 'last-total-rows', 'index': MATCH}, 'data'),

        ],
        [
            State({'type': 'anim-slider', 'index': MATCH}, 'value'),
            State({'type': 'my-index', 'index': MATCH}, 'data'),
            State({'type': 'redis-timestamp', 'index': MATCH}, 'data'),
        ]
        # prevent_initial_call=True
    )
    def update_celery_data(interval,rows, slider, index, now):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        if input_type == 'celery-interval':
            try:
                print(f'checking {index}-{now}')
                result = redis_instance.get(f'{index}-{now}').decode("utf-8")
                result = json.loads(result)
                ctx = dash.callback_context
                input_index = get_ctx_index(ctx)
                # get max and min of current frame
                count = {
                    MAXIMUM: result[str(slider)][MAXIMUM]['count'],
                    MINIMUM: result[str(slider)][MINIMUM]['count'],
                }
                # print('done bro', now)
                print(f'done {index}-{now}')

                return result, True, collapse_markup(input_index, count)
            except Exception as e:
                print('celery', e)
                return dash.no_update, False, dash.no_update
        elif input_type == 'last-total-rows':
            # print('started bro', now)
            return dash.no_update, False, dash.no_update
        raise PreventUpdate


#############################################################################################################################################

# update lcelery data according to interval
def register_update_notif_body(app):
    @app.callback(
        [
            Output({'type': 'notif-body', 'index': MATCH}, 'children'),
            Output({'type': f'{MAXIMUM}-badge', 'index': MATCH}, 'children'),
            Output({'type': f'{MINIMUM}-badge', 'index': MATCH}, 'children'),

        ],
        [
            Input({'type': 'celery-data', 'index': MATCH}, 'data'),
            Input({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'last-notif-click', 'index': MATCH}, 'data')
        ],
        [
            State({'type': 'anim-slider', 'index': MATCH}, 'value'),
            State({'type': 'last-notif-click', 'index': MATCH}, 'data'),
            # State({'type': 'celery-data', 'index': MATCH}, 'data'),

        ],

        prevent_initial_call=True
    )
    def update_notif_body(cdata, slider, itype, cvalue, stype):
        if stype is None:
            raise PreventUpdate
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        # df_frame = collection.data[input_index][FRAME].unique()
        type = stype.split('-')[0]

        if input_type == 'celery-data':
            if handleOutOfRangeNotif(cdata, slider):
                return 'Loading...', '-', '-'
            notif = cdata[str(cvalue)][type]['data'] if type != '' else ''
            return notif, cdata[str(cvalue)][MAXIMUM]['count'], cdata[str(cvalue)][MINIMUM]['count']

        elif input_type == 'anim-slider' and cdata is not None:
            if handleOutOfRangeNotif(cdata, slider):
                return 'Loading...', '-', '-'
            notif = cdata[str(slider)][type]['data'] if type != '' else ''
            return notif, cdata[str(slider)][MAXIMUM]['count'], cdata[str(slider)][MINIMUM]['count']

        elif input_type == 'last-notif-click':
            if handleOutOfRangeNotif(cdata, slider):
                return 'Loading...', '-', '-'
            notif = cdata[str(slider)][type]['data'] if type != '' else ''
            return notif, cdata[str(slider)][MAXIMUM]['count'], cdata[str(slider)][MINIMUM]['count']

        else:
            raise PreventUpdate


#############################################################################################################################################

# update live interval according to live switch
def register_toggle_badge_color(app):
    @app.callback(
        [
            Output({'type': f'{MAXIMUM}-badge', 'index': MATCH}, 'color'),
            Output({'type': f'{MINIMUM}-badge', 'index': MATCH}, 'color'),
        ],
        [
            Input({'type': f'{MAXIMUM}-notif', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'{MINIMUM}-notif', 'index': MATCH}, 'n_clicks')
        ],
        [
            State({'type': 'last-notif-click', 'index': MATCH}, 'data'),
            State({'type': 'is-slided-up', 'index': MATCH}, 'data')
        ],
        prevent_initial_call=True
    )
    def toggle_badge_color(max, min, state, is_open):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
        type = input_type.split('-')[0]
        if input_type == f'{MAXIMUM}-notif' and max is not None or input_type == f'{MINIMUM}-notif' and min is not None:
            obj = {
                MAXIMUM: 'light',
                MINIMUM: 'light'
            }

            if input_type != state or (input_type == state and not is_open):
                obj[type] = 'info'
            return  obj[MAXIMUM], obj[MINIMUM]

        raise PreventUpdate


#############################################################################################################################################

def register_update_last_celery_key(app):
    @app.callback(
        [
            Output({'type': 'last-total-rows', 'index': MATCH}, 'data'),
            Output({'type': 'redis-timestamp', 'index': MATCH}, 'data'),
        ],
        [
            # Input({'type': 'celery-data', 'index': MATCH}, 'data'),
            Input({'type': 'live-mode', 'index': MATCH}, 'on'),
            Input({'type': 'live-interval', 'index': MATCH}, 'n_intervals'),
        ],
        [
            State({'type': 'last-total-rows', 'index': MATCH}, 'data'),
            State({'type': 'my_param', 'index': MATCH}, 'data')
        ],
        prevent_initial_call=True
    )
    def update_last_celery_key( live, interval, last_rows, param):
        ctx = dash.callback_context
        input_index= None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)

        if input_type == 'live-mode' and  not live:
            current_rows = len(collection.data[input_index].index)
            if last_rows < current_rows:
                now = datetime.now().timestamp()
                result = task.process_dataset.delay(input_index, collection.data[input_index].to_dict(), param['vtype'], param['parameter'], now)

                return current_rows, now

        elif input_type == 'live-interval':
            current_rows = len(collection.data[input_index].index)
            if interval != 0  and interval % 5 == 0 and last_rows < current_rows:
                now = datetime.now().timestamp()
                # print(now,' interval: ', interval, )
                result = task.process_dataset.delay(input_index, collection.data[input_index].to_dict(), param['vtype'], param['parameter'], now)
                return current_rows, now

        raise PreventUpdate


# ############################################################################################################################################

# # update live interval according to live switch
# def register_update_legend_theme(app):
#     @app.callback(
#         [
#             Output({'type': 'live-interval', 'index': MATCH}, 'disabled'),
#             Output({'type': 'play-btn', 'index': MATCH}, 'disabled'),
#         ],
#         [Input({'type': 'live-mode', 'index': MATCH}, 'on')],
#         prevent_initial_call=True
#     )
#     def update_live_mode(live):
#         return not live, live