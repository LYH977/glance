
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

from components.visual.utils.info import info_markup
from utils import collection
from utils.constant import CAROUSEL_CONSTANT, ITEM, TIME, CAROUSEL
from utils.method import set_slider_calendar, get_last_timestamp


def create_carousel(screen_height, screen_width, create_clicks, param, maxValue, df_frame, tformat, dbname):
    columns = collection.temp.columns.tolist()
    columns.remove('frame')
    last_nano = get_last_timestamp(collection.temp[TIME])

    return html.Div(
        className='visualization-container ',
        id={'type': 'visualization-container', 'index': create_clicks},

        style={
            'height': screen_height* 0.72,
           'width': screen_width/2.2,
               # 'width': '500px',
               },
        children=html.Div([
            dcc.Store(id={'type': 'my-index', 'index': create_clicks}, data=create_clicks),
            dcc.Store(id={'type': 'ca-is-animating', 'index': create_clicks}, data = False),
            # dcc.Store(id='ca-uuid', data = create_clicks),
            dcc.Store(id={'type': 'my_param', 'index': create_clicks}, data=param),
            dcc.Store(id={'type': 'frame-format', 'index': create_clicks}, data=tformat),
            dcc.Store(id={'type': 'ca-last-timestamp', 'index': create_clicks}, data=last_nano),
            dcc.Store(id={'type': 'ca-at-max', 'index': create_clicks}, data=False),
            dcc.Store(id={'type': 'ca-current-frame', 'index': create_clicks}, data=df_frame[0]),
            dcc.Store(id={'type': 'db-name', 'index': create_clicks}, data=dbname),
            dcc.Store(id={'type': 'last-edit-click-ts', 'index': create_clicks}, data=None),
            dcc.Store(id={'type': 'dataset-column-name', 'index': create_clicks}, data=columns),
            dcc.Store(id={'type': 'last-secondary-click-ts', 'index': create_clicks}, data=None),

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
                dbc.Col(ca_name_section_markup(create_clicks, dbname, CAROUSEL), width='auto'),
                dbc.Col(html.Div(
                    [
                        html.Span(
                            html.I(className="fa fa-cog fa-lg icon-btn icon-grey"),
                            id=f"popover-setting-wrapper-{create_clicks}",
                            n_clicks=0,
                        ),
                        dbc.Popover(
                            ca_popover_children_markup(create_clicks),
                            id="legacy",
                            target=f"popover-setting-wrapper-{create_clicks}",
                            trigger="legacy",
                            placement='bottom-end',
                        ),
                    ],
                ), width='auto')

            ],justify="around", align='center'),
            html.Div(
                create_ca_img(collection.temp.loc[0,param['parameter'][CAROUSEL_CONSTANT[ITEM]]]),
                id={'type': 'fade1', 'index': create_clicks},
                style={ 'height': '480px', 'width': '100%'},
            ),

            dcc.Slider(
                id={'type': 'ca-anim-slider', 'index': create_clicks},
                updatemode='drag',
                min=0,
                max=maxValue,
                value=0,
                # marks={str(i): str(des) for i, des in
                #        zip(range(0, df_frame.shape[0]), set_slider_calendar(df_frame))},
            ),
            html.Div([
                dbc.Button(
                    'play',
                    id={'type': 'ca-play-btn', 'index': create_clicks},
                    color="light",
                    size='sm',
                    className='play-btn'
                ),
                html.Label(df_frame[0], id={'type': 'ca-slider-label', 'index': create_clicks}, style={'color':'white'})
            ]),
        ]),
                )

def create_ca_img(src):
    return html.Img(
        src=src,
        style={'height': '100%', 'width': '100%', 'overflow':'hidden'}
    )


def ca_popover_children_markup(create_clicks):

    return [
        dbc.PopoverHeader(
            [
                dbc.DropdownMenuItem(divider=True),
                dbc.Row([
                    dbc.Col(daq.BooleanSwitch(
                        id={'type': 'ca-live-mode', 'index': create_clicks},
                        on=False,
                        color="#9B51E0",
                        label='Live Mode',
                    ), width='auto'),
                    dbc.Col( html.Span(
                        html.I( className="fa fa-trash fa-lg icon-btn icon-red"),
                        id={'type': 'dlt-btn', 'index': create_clicks},
                        n_clicks=0,
                    ), width='auto'),
                ], align= 'center', justify='around'),

                # daq.BooleanSwitch(
                #     id={'type': 'ca-live-mode', 'index': create_clicks},
                #     on=False,
                #     color="#9B51E0",
                #     label='Live Mode',
                # ),
                dbc.DropdownMenuItem(divider=True),

                # html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks}),

                # html.Div([
                #     html.Span(
                #         html.I( className="fa fa-trash fa-lg icon-btn icon-red"),
                #         id={'type': 'dlt-btn', 'index': create_clicks},
                #         n_clicks=0,
                #     ),
                #
                # ])


            ],
            # style={'maxWidth': '400px'},
        ),
    ]

def ca_name_section_markup(create_clicks, name1, type1):
    return html.Div([
        info_markup(create_clicks, name1, type1),
        dcc.Input(
            id={'type': 'visual-title', 'index': create_clicks},
            type="text",
            value=f'Visualization {create_clicks}',
            maxLength=18,
            autoFocus=False,
            autoComplete='off',
            size='13',
            className='visual-title'
        ),
    ], className='flex')