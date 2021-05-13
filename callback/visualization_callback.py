import json
from datetime import datetime
import pandas as pd
import dash
from dash.dependencies import Input, Output, State, MATCH, ClientsideFunction
from dash.exceptions import PreventUpdate
import plotly.express as px
import os
from geopy.geocoders import MapBox
import task
from components.visual.figures.figure_method import create_figure
from components.visual.notifications.collapse import collapse_markup
from components.visual.utils.marker import namelist_item_markup, namelist_item_not_found_markup
from utils import collection
from utils.collection import redis_instance
from utils.export.export_data import export_mp4
from utils.method import get_ctx_type, get_ctx_index, formatted_time_value, \
    select_query, get_last_timestamp, insert_marker, reset_marker_trace
from utils.constant import SCATTER_MAP, DENSITY, CHOROPLETH, BAR_CHART_RACE, \
    FRAME, TIME, MAXIMUM, MINIMUM

MAPBOX_GEOCODER = MapBox(os.environ['MAP_TOKEN'])

def handleOutOfRangeNotif(celery, slider):
    length = len(celery)
    if slider > length - 1:
        return True
    return False

def assign_style (toggle):
    if toggle:
        ostyle = {'height': '40%'}
        nstyle = { 'height': '150px'}
    else:
        ostyle = {'height': '15%'}
        nstyle = {  'height': 0, }
    return ostyle, nstyle

def check_valid_lat(input):
    try:
        value = float(input)
        if value >= -85 and value <= 85:
            return True
        return False
    except ValueError:
        return False

def check_valid_long(input):
    try:
        value = float(input)
        if value >= -180 and value <= 180:
            return True
        return False
    except ValueError:
        return False
#############################################################################################################################################


def register_update_figure(app):
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='update_figure'
        ),
        Output({'type': 'visualization', 'index': MATCH}, 'figure'),
        [
            Input({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'legend-theme', 'index': MATCH}, 'on'),
            Input({'type': 'mapbox-type', 'index': MATCH}, 'value'),
            Input({'type': 'chosen-color-scale', 'index': MATCH}, 'data'),
            Input({'type': 'marker-data', 'index': MATCH}, 'data'),

        ],
        [
            State({'type': 'my_param', 'index': MATCH}, 'data'),
            State({'type': 'at-max', 'index': MATCH}, 'data'),
            State({'type': 'live-mode', 'index': MATCH}, 'on'),
            State({'type': 'back-buffer', 'index': MATCH}, 'data'),
            # State({'type': 'visualization', 'index': MATCH}, 'figure'),
        ],
        prevent_initial_call=True
    )

#############################################################################################################################################

# update play button label according to playing status

def register_update_color_scale(app):
    @app.callback(
        Output({'type': 'chosen-color-scale', 'index': MATCH}, 'data'),
        Input({'type': 'color-scale-dropdown', 'index': MATCH}, 'value'),
        State({'type': 'chosen-color-scale', 'index': MATCH}, 'data'),
        prevent_initial_call=True
    )
    def update_color_scale(dropdown, chosen):
        if dropdown == chosen['name']:
            raise PreventUpdate
        chosen_color = eval(f'px.colors.sequential.{dropdown}')
        formatted_scale, scale = px.colors.convert_colors_to_same_type(chosen_color)
        colorscale = px.colors.make_colorscale(formatted_scale, scale=scale)
        # print(colorscale)
        return {'name': dropdown, 'value': colorscale}

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
            # Output({'type': 'interval', 'index': MATCH}, 'n_intervals'),
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
        df_frame = collection.data[input_index][FRAME].unique()
        maxValue = df_frame.shape[0] - 1
        if input_type == 'anim-slider':  # input from slider
            label = df_frame[s_value]

            # if playing is True and s_value != interval:
            #     print('1st condition true: ', s_value, ' and ',interval)
            # if  s_value == maxValue:
            #     print('2nd condition true')

            return \
                False if playing is True and s_value != interval or s_value == maxValue else dash.no_update, \
                label

        elif input_type == 'play-btn':  # input from play btn
            return \
                not playing, \
                dash.no_update

        elif input_type == 'live-mode':  # input from play btn
            return \
                False if live is True else dash.no_update, \
                dash.no_update

        raise PreventUpdate

#############################################################################################################################################

def register_reset_slider_n_interval(app):
    @app.callback(
        Output({'type': 'interval', 'index': MATCH}, 'n_intervals'),
        Input({'type': 'play-btn', 'index': MATCH}, 'n_clicks'),
        State({'type': 'anim-slider', 'index': MATCH}, 'value'),

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
        df_frame = collection.data[input_index][FRAME].unique()
        maxValue = df_frame.shape[0] - 1
        return slider if slider != maxValue else 0
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
            Input({'type': 'mapbox-type', 'index': MATCH}, 'value'),
            Input({'type': 'chosen-color-scale', 'index': MATCH}, 'data'),
            Input({'type': 'marker-data', 'index': MATCH}, 'data'),

        ],
        [
            State({'type': 'last-timestamp', 'index': MATCH}, 'data'),
            State({'type': 'frame-format', 'index': MATCH}, 'data'),
            State({'type': 'my_param', 'index': MATCH}, 'data'),
            State({'type': 'db-name-0', 'index': MATCH}, 'data'),
            State({'type': 'back-buffer', 'index': MATCH}, 'data'),
            State({'type': 'new-column-info', 'index': MATCH}, 'data'),

        ],
        prevent_initial_call=True
    )
    def update_live_data(live, legend,mapbox, colorscale, marker, ts, format,  param, dbname, buffer, info):
        ctx = dash.callback_context
        input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            input_index = get_ctx_index(ctx)
        if input_type =='live-interval' and collection.live_processing[input_index] is False:
            collection.live_processing[input_index] = True
            result = select_query(dbname, 'where time >{}'.format(ts))
            if result is not None:
                result[TIME] = result.index.map(lambda x: str(x).split('+')[0])
                result[FRAME] = result[TIME].map(lambda x: formatted_time_value(x, format))
                copydf = result.copy(deep=True)
                for col in info['numeric_col']:
                    copydf[col] = pd.to_numeric(copydf[col])
                for exp in info['expression']:
                    new_col = copydf.eval( exp['equation'])
                    result[ exp['name'] ] = new_col
                last_nano = get_last_timestamp(result[TIME])
                collection.data[input_index] = collection.data[input_index].append(result, ignore_index=True)
                fig = create_figure(collection.data[input_index], param['parameter'], param['vtype'])
                return last_nano, fig
            collection.live_processing[input_index] = False
            raise PreventUpdate

        elif input_type == 'legend-theme':
            fig2 = buffer
            if legend : #dark theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(0,0,0,1)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(255,255,255,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(255,255,255,1)'
                # fig2['layout']['paper_bgcolor'] = '#000'

            else: # light theme
                fig2['layout']['coloraxis']['colorbar']['bgcolor'] = 'rgba(255,255,255,1)'
                fig2['layout']['coloraxis']['colorbar']['title']['font']['color'] = 'rgba(0,0,0,1)'
                fig2['layout']['coloraxis']['colorbar']['tickfont']['color'] = 'rgba(0,0,0,1)'
                # fig2['layout']['paper_bgcolor'] = '#fff'

            return dash.no_update,fig2

        elif input_type == 'mapbox-type':
            fig2 = buffer
            fig2['layout']['mapbox']['style'] = mapbox
            return dash.no_update, fig2

        elif input_type == 'chosen-color-scale':
            fig2 = buffer
            fig2['layout']['coloraxis']['colorscale'] = colorscale['value']

            # fig2['data'][1] = insert_marker()
            return dash.no_update, fig2

        elif input_type == 'marker-data':
            fig2 = buffer
            fig2['data'][1] = marker
            return dash.no_update, fig2

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
        # input_index = None
        if not ctx.triggered:
            input_type = 'No input yet'
        else:
            input_type = get_ctx_type(ctx)
            # input_index = get_ctx_index(ctx)
        if input_type == 'celery-interval':
            try:
                # print(f'checking {index}-{now}')
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
                # print(f'done {index}-{now}')
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
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='update_notif_body'
        ),
        [
            Output({'type': 'notif-body', 'index': MATCH}, 'children'),
            Output({'type': f'{MAXIMUM}-badge', 'index': MATCH}, 'children'),
            Output({'type': f'{MINIMUM}-badge', 'index': MATCH}, 'children')
        ],

        [
            Input({'type': 'celery-data', 'index': MATCH}, 'data'),
            Input({'type': 'anim-slider', 'index': MATCH}, 'value'),
            Input({'type': 'last-notif-click', 'index': MATCH}, 'data'),
        ],

        prevent_initial_call=True
    )



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
                result = task.process_dataset.delay(input_index, collection.data[input_index].to_dict(), param['vtype'], param['parameter'], now)
                return current_rows, now

        raise PreventUpdate


# ############################################################################################################################################

def register_export_visual(app):
    @app.callback(
        [
            Output({'type': 'export-link', 'index': MATCH}, 'download'),
            Output({'type': 'export-link', 'index': MATCH}, 'href'),
            Output({'type': 'export-link-wrapper', 'index': MATCH}, 'style'),
            Output({'type': 'export-btn', 'index': MATCH}, 'hidden'),
        ],
        [Input({'type': 'export-btn', 'index': MATCH}, 'disabled')],
        [
            State({'type': 'export-name', 'index': MATCH}, 'data'),
            State({'type': 'visualization', 'index': MATCH}, 'figure')
        ],
        prevent_initial_call=True
    )
    def export_visual(disabled, name, fig):
        # print(fig)
        if disabled:
            export_mp4(fig, name)
            dl = f'{name}.mp4'
            path = app.get_asset_url(f'export/{dl}')

            print(f'habis href {name}')
            return dl, path, {'display': 'block'}, True
        return None, None, {'display': 'none'}, dash.no_update

# ############################################################################################################################################

def register_handle_export_btn_click(app):
    @app.callback(
        [
            Output({'type': 'export-btn', 'index': MATCH}, 'disabled'),
            Output({'type': 'export-interval', 'index': MATCH}, 'disabled'),
            Output({'type': 'export-name', 'index': MATCH}, 'data'),
        ],
        [Input({'type': 'export-btn', 'index': MATCH}, 'n_clicks')],
        [
            State({'type': 'export-btn', 'index': MATCH}, 'disabled'),
        ],
        prevent_initial_call=True
    )
    def handle_export_btn_click(btn_click, disabled):
        if btn_click and not disabled:
            now = int(datetime.now().timestamp())
            # print('btn part')
            return True, False, now

        raise PreventUpdate


# ############################################################################################################################################

def register_reset_export_interval(app):
    @app.callback(
        Output({'type': 'export-interval', 'index': MATCH}, 'n_intervals'),
        [Input({'type': 'export-link', 'index': MATCH}, 'n_clicks')],
        prevent_initial_call=True
    )
    def reset_export_interval(click):
        return 0

# ############################################################################################################################################

def register_update_marker_namelist(app):
    @app.callback(
        Output({'type': 'marker-namelist', 'index': MATCH}, 'children'),
        Input({'type': 'marker-search-name', 'index': MATCH}, 'value'),
        [
            # State({'type': 'marker-data', 'index': MATCH}, 'data'),
            State({'type': 'my-index', 'index': MATCH}, 'data'),
        ],

        prevent_initial_call=True
    )
    def update_marker_namelist(value,  index):
        if len(value.strip()) == 0:
            raise PreventUpdate
        try:
            results = MAPBOX_GEOCODER.geocode(query=value, exactly_one=False, )
            namelist = []
            # if len(marker['lat']) !=0: # if marker is specified
            #     namelist.append(namelist_marked_item_markup(marker['name'],marker['coordinate']))
            for result,id in zip(results, range(0, len(results))):
                raw = result.raw
                lat = raw['geometry']['coordinates'][1]
                long = raw['geometry']['coordinates'][0]
                coordinate = f"({lat}, {long})"
                temp = namelist_item_markup(raw['place_name'], coordinate, id, index)
                namelist.append(temp)

            return namelist
        except Exception as e:
            print(e)
            return [namelist_item_not_found_markup(value)]

# ############################################################################################################################################

def register_update_marker_data(app):
    @app.callback(
        Output({'type': 'marker-data', 'index': MATCH}, 'data'),
        [
            Input({'type': 'marker-name-section-data', 'index': MATCH}, 'data'),
            Input({'type': 'reset-marker-btn', 'index': MATCH}, 'n_clicks'),
            Input({'type': 'coordinate-apply-btn', 'index': MATCH}, 'n_clicks'),

        ],
        [
            State({'type': 'latitude', 'index': MATCH}, 'value'),
            State({'type': 'longitude', 'index': MATCH}, 'value'),
        ],
        prevent_initial_call=True
    )
    def update_marker_data(name, reset, apply, lat, long):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)
        if input_type == 'marker-name-section-data':
            return name
        elif input_type == 'reset-marker-btn':
            return reset_marker_trace()
        elif input_type == 'coordinate-apply-btn':
            return insert_marker('unknown', f'({float(lat)}, {float(long)})')
        raise PreventUpdate

# ############################################################################################################################################

def register_update_marker_name_section_data(app):
    @app.callback(
        Output({'type': 'marker-name-section-data', 'index': MATCH}, 'data'),
        [
            Input({'type': f'marker-name-btn-0', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'marker-name-btn-1', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'marker-name-btn-2', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'marker-name-btn-3', 'index': MATCH}, 'n_clicks'),
            Input({'type': f'marker-name-btn-4', 'index': MATCH}, 'n_clicks'),

        ],
        [
            State({'type': f'marker-name-0', 'index': MATCH}, 'children') ,
            State({'type': f'marker-name-1', 'index': MATCH}, 'children'),
            State({'type': f'marker-name-2', 'index': MATCH}, 'children'),
            State({'type': f'marker-name-3', 'index': MATCH}, 'children'),
            State({'type': f'marker-name-4', 'index': MATCH}, 'children'),
            State({'type': f'marker-coordinate-0', 'index': MATCH}, 'children'),
            State({'type': f'marker-coordinate-1', 'index': MATCH}, 'children'),
            State({'type': f'marker-coordinate-2', 'index': MATCH}, 'children'),
            State({'type': f'marker-coordinate-3', 'index': MATCH}, 'children'),
            State({'type': f'marker-coordinate-4', 'index': MATCH}, 'children'),
        ],
        prevent_initial_call=True
    )
    def update_marker_name_section_data(btn0, btn1, btn2, btn3, btn4, name0, name1, name2, name3, name4, coo0, coo1, coo2, coo3, coo4):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_type = get_ctx_type(ctx)
        last_char = input_type[-1]
        if eval(f'btn{last_char}') is not None:
            name = eval(f'name{last_char}')
            coo =  eval(f'coo{last_char}')
            return insert_marker(name, coo)
        raise PreventUpdate



# ############################################################################################################################################

def register_update_marker_marked_name(app):
    @app.callback(
        [
            Output({'type': 'marked-name', 'index': MATCH}, 'children'),
            Output({'type': 'marked-coordinate', 'index': MATCH}, 'children'),
            Output({'type': 'marker-marked-name', 'index': MATCH}, 'style'),

        ],
        Input({'type': 'marker-data', 'index': MATCH}, 'data'),
        prevent_initial_call=True
    )
    def update_marker_marked_name(marker):
        if len(marker['lat']) != 0:  # if marker is specified
            name = marker['name']
            coordinate = marker['coordinate']
            style= {'display':'block'}
        else:
            name = ''
            coordinate = ''
            style = {'display': 'none'}
        return name, coordinate, style

# ############################################################################################################################################

def register_reset_lat_long(app):
    @app.callback(
        [
            Output({'type': 'latitude', 'index': MATCH}, 'value'),
            Output({'type': 'longitude', 'index': MATCH}, 'value'),
        ],
        Input({'type': 'reset-marker-btn', 'index': MATCH}, 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_export_interval(reset):
        return '',''

# ############################################################################################################################################



def register_toggle_coordinate_apply_btn(app):
    @app.callback(
        Output({'type': 'coordinate-apply-btn', 'index': MATCH}, 'disabled'),
        [
            Input({'type': 'latitude', 'index': MATCH}, 'value'),
            Input({'type': 'longitude', 'index': MATCH}, 'value'),
        ],
        prevent_initial_call=True
    )
    def toggle_coordinate_apply_btn(lat, long):
        if check_valid_lat(lat) and check_valid_long(long):
            return False
        return True