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

def change_frame(ftype,fig2, value ):
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


# update visualization container by appending or removing item from array
def register_update_visual_container(app):
    @app.callback(
         Output('visual-container', 'children') ,
        [ Input('create', 'n_clicks'), Input({'type':'dlt-btn', 'index': ALL},'n_clicks') ],
        [ State('visual-container', 'children') , State('last-param', 'data'),  State('time-format', 'value')    ],
        prevent_initial_call=True)
    def update_visual_container(create_clicks, deletable, div_children, param, tformat):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            # input_type = get_ctx_type(ctx)

        if input_type == 'create': # input from add button
            collection.temp = collection.temp.dropna()
            collection.temp.reset_index(drop=True, inplace=True)
            collection.temp[FRAME] = collection.temp[TIME].map(lambda x: formatted_time_value(x, tformat))
            collection.data[create_clicks] = collection.temp
            collection.live_processing[create_clicks] = False

            # if param['vtype'] != CAROUSEL:
            #     task.process_dataset(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'])

                # result = task.process_dataset.delay(create_clicks, collection.temp.to_dict(), param['vtype'], param['parameter'])
                # print('result first', result.status)

            new_child = container.render_container(create_clicks, param['parameter'], param['vtype'], tformat)
            div_children.append(new_child)
            visual_container.append(create_clicks)

            return div_children
        else: # input from delete button
            delete_index = get_ctx_index(ctx)
            temp = visual_container.index(delete_index)
            del div_children[temp]
            del visual_container[temp]
            return div_children


#############################################################################################################################################


# update  figure according to slider
def register_update_figure(app):
    @app.callback(
        Output({'type':'visualization', 'index': MATCH}, 'figure') ,
        [Input({'type':'anim-slider', 'index': MATCH}, 'value'), Input({'type':'last-timestamp', 'index': MATCH}, 'data')],
        [
            State({'type':'visualization', 'index': MATCH}, 'figure'),
            State({'type':'figure-type', 'index': MATCH}, 'data') ,
            State({'type': 'live-temp', 'index': MATCH}, 'data'),
            State({'type': 'anim-slider', 'index': MATCH}, 'max'),
            State({'type': 'anim-slider', 'index': MATCH}, 'value')
        ],
        prevent_initial_call = True)
    def update_figure(value, ts, fig, ftype, new_fig, smax, svalue):
        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index=get_ctx_index(ctx)
        if input_type =='anim-slider':
            fig2 = fig
            change_frame(ftype, fig2, value)
            return fig2
        elif input_type=='last-timestamp':
            # collection.live_processing[input_index] = True
            if smax == svalue:
                new_max = len(new_fig['frames'])
                change_frame(ftype, new_fig, new_max-1)
            return  new_fig


############################################################################################################################################## update slider according to interval
def register_update_slider(app):
    @app.callback(
        [Output({'type':'anim-slider', 'index': MATCH}, 'value'), Output({'type':'anim-slider', 'index': MATCH}, 'max'), Output({'type':'interval', 'index': MATCH}, 'max_intervals')],
        [Input({'type':'interval', 'index': MATCH}, 'n_intervals'), Input({'type':'last-timestamp', 'index': MATCH}, 'data')],
        [
            State({'type':'is-animating', 'index': MATCH}, 'data'),
            State({'type': 'anim-slider', 'index': MATCH}, 'max'),
            State({'type': 'anim-slider', 'index': MATCH}, 'value')
        ]
    )
    def update_slider(value,ts, animate, smax, svalue):
        ctx = dash.callback_context
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)

        if input_type == 'interval':
            if animate is True:
                return value, dash.no_update
            else:
                raise PreventUpdate
        elif input_type == 'last-timestamp':
            input_index = get_ctx_index(ctx)
            df_frame = collection.data[input_index][FRAME].unique()
            maxValue = df_frame.shape[0] - 1
            collection.live_processing[input_index] = False
            return \
                maxValue if smax == svalue else dash.no_update,\
                maxValue,\
                maxValue
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
        [
            State({'type':'is-animating', 'index': MATCH}, 'data'),
            State({'type':'interval', 'index': MATCH}, 'n_intervals'),
            # State({'type':'my_param', 'index': MATCH}, 'data'),
            State({'type':'figure-type', 'index': MATCH}, 'data'),
            # State({'type': 'my_tformat', 'index': MATCH}, 'data')

        ],
        prevent_initial_call=True
    )
    def update_playing_status(play_clicked, s_value, playing, interval, ftype):
        ctx = dash.callback_context
        input_index=None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index=get_ctx_index(ctx)
        # print('param', param)
        df_frame = collection.data[input_index][FRAME].unique()
        maxValue = df_frame.shape[0] - 1
        if input_type== 'anim-slider': #input from slider
            label = df_frame[s_value]
            return \
                False if playing is True and s_value != interval or s_value == maxValue else dash.no_update,\
                dash.no_update, \
                label

        elif  input_type== 'play-btn':#input from play btn
            return \
                not playing, \
                s_value if s_value != maxValue else 0, \
                dash.no_update

        else:
            raise PreventUpdate

#############################################################################################################################################

# update live interval according to live switch
def register_update_live_interval(app):
    @app.callback(
        Output({'type':'live-interval', 'index': MATCH}, 'disabled'),
        [Input({'type':'live-mode', 'index': MATCH}, 'on')],

        prevent_initial_call=True
    )
    def update_live_interval(live):

        return not live


#############################################################################################################################################

# fetch new data for live mode
def register_update_live_data(app):
    @app.callback(
        [Output({'type':'last-timestamp', 'index': MATCH}, 'data'),Output({'type':'live-temp', 'index': MATCH}, 'data')],
        [Input({'type':'live-interval', 'index': MATCH}, 'n_intervals')],
        [
            State({'type':'last-timestamp', 'index': MATCH}, 'data'),
            State({'type':'frame-format', 'index': MATCH}, 'data'),
            State({'type': 'figure-type', 'index': MATCH}, 'data'),
            State({'type': 'my_param', 'index': MATCH}, 'data')
        ],
        prevent_initial_call=True
    )
    def update_live_data(live, ts, format, ftype, param):
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
            # last_nano = get_last_timestamp(collection.data[input_index][TIME])
            # print(live,',',result)
            if result is not None:

                result[TIME] = result.index.map(lambda x: str(x).split('+')[0])
                result[FRAME] = result[TIME].map(lambda x: formatted_time_value(x, format))
                # result.reset_index(drop=True, inplace=True)
                last_nano = get_last_timestamp(result[TIME])
                collection.data[input_index] = collection.data[input_index].append(result, ignore_index=True)
                fig = create_figure(collection.data[input_index], param, ftype)

                return last_nano,fig
            else:
                collection.live_processing[input_index] = False

                raise PreventUpdate

