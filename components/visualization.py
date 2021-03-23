from datetime import datetime
import tkinter as tk

import dash
import pandas as pd                  # for DataFrames
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

import os

from utils import collection
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    SCATTER_MAP_CONSTANT, LATITUDE, LONGITUDE, SIZE, COLOR, NAME, FRAME, MESSAGE, SCATTER_GEO_CONSTANT, \
    BAR_CHART_RACE_CONSTANT, ITEM, VALUE, DENSITY_CONSTANT, Z, CHOROPLETH_CONSTANT, LOCATIONS, STANDARD_T_FORMAT, TIME, \
    MAXIMUM, MINIMUM, VISUAL_HEIGHT, COLLAPSE_HEIGHT
from raceplotly.plots import barplot

from utils.method import set_slider_calendar, formatted_time_value, to_nanosecond_epoch, get_last_timestamp

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)
root = tk.Tk()
swidth = root.winfo_screenwidth()
# data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
# data = pd.read_csv(data_url)

def create_figure(data, parameter, ftype):
    if ftype == SCATTER_MAP:
        return create_scattermap(data,parameter)
    elif ftype == SCATTER_GEO:
        return create_scatter_geo(data,parameter)
    elif ftype == BAR_CHART_RACE:
        return create_bar_chart_race(data, parameter)
    elif ftype == DENSITY:
        return create_density(data, parameter)
    elif ftype == CHOROPLETH:
        return create_choropleth(data, parameter)



def configure_fig(fig):
    # print(fig)
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
    # fig.layout.coloraxis.showscale = False

    fig.layout.coloraxis.colorbar.len = 0.5
    fig.layout.coloraxis.colorbar.yanchor = 'bottom'
    fig.layout.coloraxis.colorbar.xpad = 10
    fig.layout.coloraxis.colorbar.x =0
    fig.layout.coloraxis.colorbar.thickness = 10

    #dark theme legend
    # fig.layout.coloraxis.colorbar.bgcolor = 'rgba(0,0,0,0.5)'
    # fig.layout.coloraxis.colorbar.title.font.color = 'rgba(255,255,255,1)'
    # fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(255,255,255,1)'

    #white theme legend
    fig.layout.coloraxis.colorbar.bgcolor = 'rgba(255,255,255,0.5)'
    fig.layout.coloraxis.colorbar.title.font.color = 'rgba(0,0,0,1)'
    fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(0,0,0,1)'

    fig.layout.margin.t = 0
    fig.layout.margin.b = 0
    fig.layout.margin.r = 0
    fig.layout.margin.l = 0
    fig.layout.updatemenus[0].showactive = True

    fig['layout']['uirevision'] = 1
    # fig.layout.autosize = False

def convert_to_float(data, parameter, list):
    for i in list:
        data[parameter[i]] = data[parameter[i]].astype(float)


def create_scattermap(data, parameter):
    convert_to_float(data, parameter, [
        SCATTER_MAP_CONSTANT[LATITUDE],
        SCATTER_MAP_CONSTANT[LONGITUDE]
    ])
    fig = px.scatter_mapbox(
        data, lat = parameter[SCATTER_MAP_CONSTANT[LATITUDE]],
        lon = parameter[SCATTER_MAP_CONSTANT[LONGITUDE]],
        size = parameter[SCATTER_MAP_CONSTANT[SIZE]], size_max = 50,
        color = parameter[SCATTER_MAP_CONSTANT[COLOR]], color_continuous_scale = px.colors.sequential.Pinkyl,
        hover_name = parameter[SCATTER_MAP_CONSTANT[NAME]],
        mapbox_style = 'dark', zoom=1,
        animation_frame = FRAME,
        # animation_group="Province/State",
        # width=swidth ,

        hover_data = parameter[SCATTER_MAP_CONSTANT[MESSAGE]]
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig


def create_scatter_geo(data, parameter):
    convert_to_float(data, parameter, [
        SCATTER_GEO_CONSTANT[LATITUDE],
        SCATTER_GEO_CONSTANT[LONGITUDE]
    ])
    fig = px.scatter_geo(
        data, lat = parameter[ SCATTER_GEO_CONSTANT[LATITUDE] ] ,
        lon = parameter[SCATTER_GEO_CONSTANT[LONGITUDE]],
        size = parameter[SCATTER_GEO_CONSTANT[SIZE]],
        color = parameter[SCATTER_GEO_CONSTANT[COLOR]],
        hover_name = parameter[SCATTER_GEO_CONSTANT[NAME]],
        animation_frame = FRAME,
        hover_data = parameter[SCATTER_GEO_CONSTANT[MESSAGE]],
        projection = "natural earth"
    )
    configure_fig(fig)
    return fig


def create_bar_chart_race(data, parameter):
    race_plot = barplot(
        data,
        item_column = parameter[BAR_CHART_RACE_CONSTANT[ITEM]],
        value_column = parameter[BAR_CHART_RACE_CONSTANT[VALUE]],
        time_column = FRAME
    )
    fig = race_plot.plot(title = 'Top 10 Crops from 1961 to 2018',
                             item_label = 'Top 10 crops',
                             value_label = 'Production quantity (tonnes)',
                             frame_duration = 800)
    configure_fig(fig)
    return fig


def create_density(data, parameter):
    convert_to_float(data, parameter, [
        DENSITY_CONSTANT[LATITUDE],
        DENSITY_CONSTANT[LONGITUDE],
        DENSITY_CONSTANT[Z]
    ])
    fig = px.density_mapbox(
        data,
        lat = parameter[DENSITY_CONSTANT[LATITUDE]],
        lon = parameter[DENSITY_CONSTANT[LONGITUDE]],
        z = parameter[DENSITY_CONSTANT[Z]],
        hover_data=parameter[DENSITY_CONSTANT[MESSAGE]],
        radius = 10,
        center = dict(lat = 0, lon = 180),
        zoom = 0,
        animation_frame = FRAME,
        mapbox_style = "dark",
        # height= 200
    )
    configure_fig(fig)
    return fig


def create_choropleth(data,parameter):
    fig = px.choropleth(
        data, locations = parameter[CHOROPLETH_CONSTANT[LOCATIONS]],
        color = parameter[CHOROPLETH_CONSTANT[COLOR]],
        hover_name = parameter[CHOROPLETH_CONSTANT[NAME]],
        # animation_frame = parameter[CHOROPLETH_CONSTANT[FRAME]],
        animation_frame = FRAME,
        # animation_group="Province/State",
        # height = 600,
        hover_data = parameter[CHOROPLETH_CONSTANT[MESSAGE]],
        color_continuous_scale=px.colors.sequential.Plasma,
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig

def create_visualization(screen_height, screen_width, create_clicks,  param, maxValue, df_frame, tformat,dbname, now):
    last_nano = get_last_timestamp(collection.temp[TIME])
    figure = create_figure(collection.data[create_clicks], param['parameter'], param['vtype'])
    total_rows = len(collection.data[create_clicks].index)
    return html.Div(
        className='visualization-container',
        style={
            'height': screen_height* 0.72,
            'width': screen_width/2.2,
            'position': 'relative',
               },
        children=html.Div([
            dcc.Store(id={'type': 'my-index', 'index': create_clicks}, data=create_clicks),
            dcc.Store(id={'type': 'is-animating', 'index': create_clicks}, data = False),
            # dcc.Store(id={'type': 'figure-type', 'index': create_clicks}, data = ftype),
            dcc.Store(id={'type': 'my_param', 'index': create_clicks}, data = param),
            dcc.Store(id={'type': 'back-buffer', 'index': create_clicks}, data = figure),
            dcc.Store(id={'type': 'frame-format', 'index': create_clicks}, data = tformat),
            dcc.Store(id={'type': 'last-timestamp', 'index': create_clicks}, data = last_nano),
            dcc.Store(id={'type': 'at-max', 'index': create_clicks}, data = False),
            dcc.Store(id={'type': 'last-notif-click', 'index': create_clicks}, data= ''),
            dcc.Store(id={'type': 'celery-data', 'index': create_clicks}, data = None),
            dcc.Store(id={'type': 'current-frame', 'index': create_clicks}, data=df_frame[0]),
            dcc.Store(id={'type': 'db-name', 'index': create_clicks}, data=dbname),
            dcc.Store(id={'type': 'redis-timestamp', 'index': create_clicks}, data = now),
            dcc.Store(id={'type': 'last-total-rows', 'index': create_clicks}, data= total_rows),
            dcc.Store(id={'type': 'is-slided-up', 'index': create_clicks}, data= False),

            dcc.Interval(
                id={'type': 'interval', 'index': create_clicks},
                interval=200,
                n_intervals=0,
                max_intervals=maxValue,
                disabled=True
            ),
            dcc.Interval(
                id={'type': 'live-interval', 'index': create_clicks},
                interval=2000,
                n_intervals=0,
                disabled=True
            ),
            dcc.Interval(
                id={'type': 'celery-interval', 'index': create_clicks},
                interval=2000,
                n_intervals=0,
            ),
            dbc.Row([
                dbc.Col(html.Label(create_clicks)),
                # dbc.Input(
                #     id={'type': 'input', 'index': create_clicks},
                #     type="text",
                #     value=f'Visualization {create_clicks}',
                #     minLength =2,
                #     maxLength= 20
                # ),
                dcc.Input(
                    id={'type': 'input', 'index': create_clicks},
                    type="text",
                    value=f'Visualization {create_clicks}',
                    maxLength=20,
                    autoFocus= False,
                    autoComplete= False
                ),
                dbc.Col(daq.BooleanSwitch(
                    id={'type': 'live-mode', 'index': create_clicks},
                    on=False,
                    color="#9B51E0"
                )),
                dbc.Col(html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks})),

            ]),
            dcc.Graph(
                # responsive= False,
                className='visualization',
                id={'type': 'visualization', 'index': create_clicks},
                figure = figure,
                # style={
                #     # 'height': VISUAL_HEIGHT + COLLAPSE_HEIGHT,
                #     'height': '80%',
                #        },
                config={
                    # 'modeBarButtonsToRemove': ['pan2d','select2d', 'lasso2d', 'zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox','toggleHover','toImage'],
                    'displaylogo': False,
                    # 'responsive': False,
                    'displayModeBar': False
                }
            ),
            html.Div(
                id={'type': 'option-wrapper', 'index': create_clicks},
                className= 'option-wrapper',
                style={
                    'height': '15%', #40% including card body

                },
                children=[
                    dbc.Row([
                        dbc.Col(html.Button('play', id={'type': 'play-btn', 'index': create_clicks}), width='auto'),
                        dbc.Col(html.Label(df_frame[0], id={'type': 'slider-label', 'index': create_clicks},
                                           style={'color': 'white'}), width='auto'),
                        dbc.Col(dcc.Slider(
                            id={'type': 'anim-slider', 'index': create_clicks},
                            updatemode='drag',
                            min=0,
                            max=maxValue,
                            value=0,
                            # marks={str(i): str(des) for i, des in
                            #        zip(range(0, df_frame.shape[0]), set_slider_calendar(df_frame))},
                        )),
                    ]),

                    html.Div(
                        id={'type': "loading-notif-output", 'index': create_clicks},
                        children=dbc.Spinner(
                            color="light",
                            type="grow"
                        ),
                    ),
                ]
            ),

        ],style={
            'height': '100%',
            'width': '100%',
            'position': 'relative',
               },
        ),
    )





def collapse_markup(create_clicks, count):
    return html.Div([
        html.Div(
            dbc.Row(
                [
                    notif_badge_markup(MAXIMUM, count[MAXIMUM], create_clicks),
                    notif_badge_markup(MINIMUM, count[MINIMUM], create_clicks),
                ],
                no_gutters=True,
                align='start',
            ),
            style={'overflowX': 'auto'}

        ),
        html.Div(
            id={'type': 'notif-body-wrapper', 'index': create_clicks},
            className='notif-body-wrapper',
            style={'display': 'hidden', 'height': '0'  },
            children=html.Div(
                id={'type': 'notif-body', 'index': create_clicks},
                className='notif-body',

        )
        ),

    ])


def notif_badge_markup(id, number, create_clicks):
    return dbc.Col(
        dbc.Button(
            [id, dbc.Badge(number, color='light', className="ml-1", pill=True, id={'type': f'{id}-badge', 'index': create_clicks})],
            color="dark",
            id={'type': f'{id}-notif', 'index': create_clicks},
        ),
        width='auto',
        className= 'notif-badge'
    )