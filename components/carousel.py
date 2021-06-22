
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

from components.visual.container.visual_mask import visual_mask_markup
from components.visual.utils.info import info_markup
from utils import collection
from utils.constant import CAROUSEL_CONSTANT, ITEM, TIME, CAROUSEL, FRAME
from utils.method import set_slider_calendar, get_last_timestamp


def create_carousel(screen_height, screen_width, create_clicks, param, maxValue, df_frame, tformat, dbname):
    # columns = collection.temp.columns.tolist()
    # columns.remove('frame')
    # last_nano = get_last_timestamp(collection.temp[TIME])

    return html.Div(
        className='visualization-container ',
        id={'type': 'visualization-container', 'index': create_clicks},
        style={

               # 'width': '500px',
               },
        children =  html.Div([
            visual_mask_markup(create_clicks),
            ca_visual_box_markup(create_clicks, param, tformat, df_frame, dbname, maxValue)
        ])
    )




def create_ca_img(src, date='None'):
    return [
        html.Img(
            src=src,
            className='ca-img-style'
        ),
        html.P(
            date,
            className='ca-label-style',
        )
    ]


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

                    dbc.Col(html.Div([
                        ca_generate_btn_markup(create_clicks),
                        ca_download_btn_markup(create_clicks),
                        ca_enable_generate_markup(create_clicks)
                    ], className='flex-col')),


                ], align= 'center', justify='around'),

                dbc.DropdownMenuItem(divider=True),

                html.Span(
                    html.I(className="fa fa-trash fa-lg icon-btn icon-red"),
                    id={'type': 'dlt-btn', 'index': create_clicks},
                    n_clicks=0,
                ),

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
            value=f'Carousel {create_clicks}',
            maxLength=18,
            autoFocus=False,
            autoComplete='off',
            size='13',
            className='visual-title'
        ),
    ], className='flex')



def ca_generate_btn_markup(create_clicks):
    return dbc.Button(
            'Generate MP4',
            id={'type': 'ca-generate-btn', 'index': create_clicks},
            color="info",
            size='sm',
    )

def ca_download_btn_markup(create_clicks):
    return html.Div(
        html.A(
            'Download MP4',
            id={'type': 'ca-download-btn', 'index': create_clicks},
            style={'width': '50%'},
        ),
        className='export-link',
        style = {'display': 'none' },
        id={'type': 'ca-download-btn-wrapper', 'index': create_clicks},
    )

def ca_enable_generate_markup(create_clicks):
    return dbc.Button(
            'Generate Again',
            id={'type': 'ca-regenerate-btn', 'index': create_clicks},
            color="link",
            className="regenerate-btn shadow-none",
            size= 'sm',
            style={'display':'none'},
    )


def ca_visual_box_markup(create_clicks, param, tformat, df_frame, dbname, maxValue):
    columns = collection.temp.columns.tolist()
    columns.remove('frame')
    last_nano = get_last_timestamp(collection.temp[TIME])
    return html.Div(
        className='visual-box',
        children =[

        dcc.Store(id={'type': 'ca-export-name', 'index': create_clicks}, data=None),
        dcc.Store(id={'type': 'my-index', 'index': create_clicks}, data=create_clicks),
        dcc.Store(id={'type': 'ca-is-animating', 'index': create_clicks}, data=False),
        dcc.Store(id={'type': 'my_param', 'index': create_clicks}, data=param),
        dcc.Store(id={'type': 'frame-format', 'index': create_clicks}, data=tformat),
        dcc.Store(id={'type': 'ca-last-timestamp', 'index': create_clicks}, data=last_nano),
        dcc.Store(id={'type': 'ca-at-max', 'index': create_clicks}, data=False),
        dcc.Store(id={'type': 'ca-current-frame', 'index': create_clicks}, data=df_frame[0]),
        dcc.Store(id={'type': 'db-name', 'index': create_clicks}, data=dbname),
        dcc.Store(id={'type': 'last-edit-click-ts', 'index': create_clicks}, data=None),
        dcc.Store(id={'type': 'dataset-column-name', 'index': create_clicks}, data=columns),
        dcc.Store(id={'type': 'last-secondary-visual-click-ts', 'index': create_clicks}, data=None),
        dcc.Store(id={'type': 'last-secondary-toast-ts', 'index': create_clicks}, data=None),
        dcc.Store(id={'type': 'secondary-toast', 'index': create_clicks}, data=None),
        dcc.Interval(
            id={'type': 'ca-export-interval', 'index': create_clicks},
            interval=1000,
            n_intervals=0,
            disabled=True
        ),
        dcc.Interval(
            id={'type': 'ca-interval', 'index': create_clicks},
            interval=1000,
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

        ], justify="around", align='center'),
        html.Div(
            html.Div(
                create_ca_img(
                    collection.temp.loc[0, param['parameter'][CAROUSEL_CONSTANT[ITEM]]],
                    collection.temp.loc[0, FRAME]
                ),
                id={'type': 'fade1', 'index': create_clicks},
                className='ca-img-container'
            ),
            id={'type': 'visualization', 'index': create_clicks},

        ),


        dcc.Slider(
            id={'type': 'ca-anim-slider', 'index': create_clicks},
            updatemode='drag',
            min=0,
            max=maxValue,
            value=0,
        ),
        html.Div([
            dbc.Button(
                'play',
                id={'type': 'ca-play-btn', 'index': create_clicks},
                color="light",
                size='sm',
                className='play-btn'
            ),
        ]),
    ])