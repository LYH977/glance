import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils.constant import MAPBOX_TYPES, SCATTER_MAP, CHOROPLETH, DENSITY


def setting_markup(create_clicks, type):
    hasLegend = [SCATTER_MAP, DENSITY, CHOROPLETH]
    hasMapbox = [SCATTER_MAP, DENSITY]
    hide_legend = not type in hasLegend
    hide_mapbox = not type in hasMapbox

    return dbc.DropdownMenu(
        label = 'setting',
        children = [
            legend_theme_markup(create_clicks, hide_legend) ,

            mapbox_type_markup(create_clicks, hide_mapbox) ,

            live_mode_markup(create_clicks),

            delete_btn_markup(create_clicks),

            generate_btn_markup(create_clicks),
            download_btn_markup(create_clicks),
        ],
    )





def legend_theme_markup(create_clicks, hidden):
    return html.Div([
        dbc.DropdownMenuItem(
            daq.BooleanSwitch(
                id={'type': 'legend-theme', 'index': create_clicks},
                on=False,
                color="#000000",
                label='Legend Theme'
            ),
            header=True
        ),
        dbc.DropdownMenuItem(divider=True),
    ],hidden = hidden)

def live_mode_markup(create_clicks):
    return html.Div([
        dbc.DropdownMenuItem(
            daq.BooleanSwitch(
                id={'type': 'live-mode', 'index': create_clicks},
                on=False,
                color="#9B51E0",
                label=f'Live Mode {create_clicks}'
            ),
            header=True
        ),
        dbc.DropdownMenuItem(divider=True),

    ])


def delete_btn_markup(create_clicks):
    return html.Div([
        dbc.DropdownMenuItem(
            dbc.Button(
                'Delete',
                id={'type': 'dlt-btn', 'index': create_clicks},
                color="danger",
                className="mr-1"
            ),
            header=True
        ),
        dbc.DropdownMenuItem(divider=True),

    ])

def generate_btn_markup(create_clicks):
    return dbc.DropdownMenuItem(
        dbc.Button(
            'Generate MP4',
            id={'type': 'export-btn', 'index': create_clicks},
            color="info",
            className="mr-1"
        ),
        header=True,
    )

def download_btn_markup(create_clicks):
    return dbc.DropdownMenuItem(
        html.A(
            'Download MP4',
            id={'type': 'export-link', 'index': create_clicks},
            download='1618213227.mp4',
            href='/assets/export/1618213227.mp4',  # /assets/test.mp4
            style={'width': '50%'},
        ),
        className='export-link',
        style={'display': 'none'},
        id={'type': 'export-link-wrapper', 'index': create_clicks},
    )

def mapbox_type_markup(create_clicks, hidden):
    return html.Div([
        dbc.DropdownMenuItem(
            dbc.Row([
                dbc.Col(dbc.Label("Mapbox type")),
                dbc.Col(dbc.Select(
                    id={'type': 'mapbox-type', 'index': create_clicks},
                    options=[{"label": t, "value": t} for t in MAPBOX_TYPES],
                    value='dark'
                )),

            ]),

            header=True
        ),
        dbc.DropdownMenuItem(divider=True),

    ],hidden =hidden)
