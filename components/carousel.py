
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq


from utils import collection
from utils.constant import CAROUSEL_CONSTANT, ITEM, TIME
from utils.method import set_slider_calendar, get_last_timestamp


def create_carousel(screen_height, screen_width, create_clicks, param, maxValue, df_frame, tformat, dbname):
    last_nano = get_last_timestamp(collection.temp[TIME])

    return html.Div(
        className='carousel',

        style={
            # 'height': screen_height* 0.75,
           'width': screen_width/2.2,
               # 'width': '500px',
               },
        children=html.Div([
            dcc.Store(id={'type': 'ca-is-animating', 'index': create_clicks}, data = False),
            # dcc.Store(id='ca-uuid', data = create_clicks),
            dcc.Store(id={'type': 'ca-my_param', 'index': create_clicks}, data=param),
            dcc.Store(id={'type': 'ca-frame-format', 'index': create_clicks}, data=tformat),
            dcc.Store(id={'type': 'ca-last-timestamp', 'index': create_clicks}, data=last_nano),
            dcc.Store(id={'type': 'ca-at-max', 'index': create_clicks}, data=False),
            dcc.Store(id={'type': 'ca-current-frame', 'index': create_clicks}, data=df_frame[0]),
            dcc.Store(id={'type': 'ca-db-name', 'index': create_clicks}, data=dbname),

            dcc.Interval(
                id={'type': 'ca-interval', 'index': create_clicks},
                interval=500,
                n_intervals=0,
                max_intervals=maxValue,
                disabled=True
            ),
            dcc.Interval(
                id={'type': 'ca-live-interval', 'index': create_clicks},
                interval=2000,
                n_intervals=0,
                disabled=True
            ),
            dbc.Row([
                dbc.Col(html.Label(create_clicks)),
                dbc.Col(daq.BooleanSwitch(
                    id={'type': 'ca-live-mode', 'index': create_clicks},
                    on=False,
                    color="#9B51E0"
                )),
                dbc.Col(html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks})),

            ]),
            html.Div(
                create_ca_img(collection.temp.loc[0,param[CAROUSEL_CONSTANT[ITEM]]]),
                id={'type': 'fade1', 'index': create_clicks},
                # style={ 'height':300, 'width':300 , 'background':'red'},
            ),

            dcc.Slider(
                id={'type': 'ca-anim-slider', 'index': create_clicks},
                updatemode='drag',
                min=0,
                max=maxValue,
                value=0,
                marks={str(i): str(des) for i, des in
                       zip(range(0, df_frame.shape[0]), set_slider_calendar(df_frame))},
            ),
            html.Div([
                html.Button('play', id={'type': 'ca-play-btn', 'index': create_clicks}),
                html.Label(df_frame[0], id={'type': 'ca-slider-label', 'index': create_clicks})
            ]),
        ]),
                )

def create_ca_img(src):
    return html.Img(
        src=src,
        style={'height': 300, 'width': 300}
    )