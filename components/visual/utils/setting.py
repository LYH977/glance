import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.constant import MAPBOX_TYPES, SCATTER_MAP, CHOROPLETH, DENSITY, SEQUENTIAL_COLOR

def popover_children_markup(create_clicks, type):
    hasLegend = [SCATTER_MAP, DENSITY, CHOROPLETH]
    hasMapbox = [SCATTER_MAP, DENSITY]
    hide_legend = not type in hasLegend
    hide_mapbox = not type in hasMapbox
    return [
        dbc.PopoverHeader(
            [
                dbc.DropdownMenuItem(divider=True),

                dbc.Row([

                    dbc.Col(legend_theme_markup(create_clicks, hide_legend)),
                    dbc.Col(mapbox_type_markup(create_clicks, hide_mapbox)),
                ], align= 'center'),

                dbc.DropdownMenuItem(divider=True),



                dbc.Row([
                    dbc.Col(live_mode_markup(create_clicks)),
                    dbc.Col(html.Div([
                        generate_btn_markup(create_clicks),
                        download_btn_markup(create_clicks),
                        enable_generate_markup(create_clicks)
                    ], className='flex-col')),
                ], align='center'),


                dbc.DropdownMenuItem(divider=True),
                delete_btn_markup(create_clicks),

            ],
            # style={'maxWidth': '400px'},
        ),
    ]

def setting_markup(create_clicks, type):

    return html.Div(
        [
            html.Span(
                html.I(className="fa fa-cog fa-lg icon-btn icon-grey"),
                id=f"popover-setting-wrapper-{create_clicks}",
                n_clicks=0,
                # style={'color':'#cccccc'}
            ),
            dbc.Popover(

                popover_children_markup(create_clicks, type),
                id="legacy",
                target=f"popover-setting-wrapper-{create_clicks}",
                trigger="legacy",
                placement='bottom-end',
            ),
        ],

    )


def legend_theme_markup(create_clicks, hidden):
    return html.Div([
            daq.BooleanSwitch(
                id={'type': 'legend-theme', 'index': create_clicks},
                on=False,
                color="#000000",
                label='Legend Theme'
            ),
    ],hidden = hidden)

def live_mode_markup(create_clicks):
    return html.Div([
            daq.BooleanSwitch(
                id={'type': 'live-mode', 'index': create_clicks},
                on=False,
                color="#9B51E0",
                label='Live Mode',
                disabled=False
            ),
    ])


def delete_btn_markup(create_clicks):
    return html.Div([
            html.Span(
                html.I(
                    className="fa fa-trash fa-lg icon-btn icon-red"),
                id={'type': 'dlt-btn', 'index': create_clicks},
                n_clicks=0,
            ),


    ])

def generate_btn_markup(create_clicks):
    return dbc.Button(
            'Generate MP4',
            id={'type': 'generate-btn', 'index': create_clicks},
            color="info",
            # className="mr-1",
            size='sm',
    )

def download_btn_markup(create_clicks):
    return html.Div(
        html.A(
            'Download MP4',
            id={'type': 'download-btn', 'index': create_clicks},
            # download='1618213227.mp4',
            # href='/assets/export/1618213227.mp4',
            style={'width': '50%'},
        ),
        className='export-link',
        style = {'display': 'none' },
        id={'type': 'download-btn-wrapper', 'index': create_clicks},
    )

def enable_generate_markup(create_clicks):
    return dbc.Button(
            'Generate Again',
            id={'type': 'regenerate-btn', 'index': create_clicks},
            color="link",
            className="regenerate-btn shadow-none",
            size= 'sm',
            style={'display':'none'},
    )


def mapbox_type_markup(create_clicks, hidden):
    return html.Div([
            dbc.Col([
                dbc.Row(dbc.Label("Mapbox type")),
                dbc.Row(dbc.Select(
                    id={'type': 'mapbox-type', 'index': create_clicks},
                    options=[{"label": t, "value": t} for t in MAPBOX_TYPES],
                    value='dark'
                )),
            ], align= 'center'),

    ],hidden =hidden)


def color_scale_markup(create_clicks, hidden):
    return html.Div([
                dbc.Row([
                    dbc.Col(dbc.Label("Color Scale" )),
                    dbc.Col(dbc.Select(
                        id={'type': 'color-scale-dropdown', 'index': create_clicks},
                        options=[{"label": c, "value": c} for c in SEQUENTIAL_COLOR],
                        value='Pinkyl'  # 2nd Plotly3
                    )),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Label("Color Scale 2")),
                    dbc.Col(dbc.Select(
                        id={'type': 'color-scale-dropdown-2', 'index': create_clicks},
                        options=[{"label": c, "value": c} for c in SEQUENTIAL_COLOR],
                        value='Plotly3'
                    )),
                ]),
    ],hidden =hidden)