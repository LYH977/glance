
import dash_core_components as dcc
import dash_html_components as html


from utils import collection
from utils.constant import CAROUSEL_CONSTANT, ITEM
from utils.method import set_slider_calendar


def create_carousel(screen_width, create_clicks, param, maxValue, df_frame):
    return html.Div(
                    style={'width': screen_width/2.2, 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
                    children=html.Div([
                        dcc.Store(id={'type': 'ca-is-animating', 'index': create_clicks}, data = False),
                        dcc.Store(id='ca-uuid', data = create_clicks),
                        dcc.Store(id={'type': 'ca-my_param', 'index': create_clicks}, data=param),
                        dcc.Interval(
                            id={'type': 'ca-interval', 'index': create_clicks},
                            interval=500,
                            n_intervals=0,
                            max_intervals=maxValue,
                            disabled=True
                        ),
                        html.Div(
                            create_ca_img(collection.temp.loc[0,param[CAROUSEL_CONSTANT[ITEM]]]),
                            id={'type': 'fade1', 'index': create_clicks},
                            style={ 'height':300, 'width':300 , 'background':'red'},
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
                        html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks}, style={'position':'absolute', 'top':0}),
                    ]),
                )

def create_ca_img(src):
    return html.Img(
        src=src,
        style={'height': 300, 'width': 300}
    )