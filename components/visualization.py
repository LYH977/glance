import pandas as pd                  # for DataFrames
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html

import os

from utils import collection
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    SCATTER_MAP_CONSTANT, LATITUDE, LONGITUDE, SIZE, COLOR, NAME, FRAME, MESSAGE, SCATTER_GEO_CONSTANT, \
    BAR_CHART_RACE_CONSTANT, ITEM, VALUE, DENSITY_CONSTANT, Z, CHOROPLETH_CONSTANT, LOCATIONS
from raceplotly.plots import barplot

from utils.method import set_slider_calendar

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)

# data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
# data = pd.read_csv(data_url)

def create_figure(create_clicks, parameter, ftype):
    if ftype == SCATTER_MAP:
        return create_scattermap(create_clicks,parameter)
    elif ftype == SCATTER_GEO:
        return create_scatter_geo(create_clicks,parameter)
    elif ftype == BAR_CHART_RACE:
        return create_bar_chart_race(create_clicks, parameter)
    elif ftype == DENSITY:
        return create_density(create_clicks, parameter)
    elif ftype == CHOROPLETH:
        return create_choropleth(create_clicks, parameter)



def configure_fig(fig):
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
    fig.layout.coloraxis.showscale = False
    fig.layout.margin.t = 30
    fig.layout.margin.b = 30
    fig.layout.updatemenus[0].showactive = True


def convert_to_float(data, parameter, list):
    for i in list:
        data[parameter[i]] = data[parameter[i]].astype(float)

def create_scattermap(create_clicks, parameter):
    data = collection.data[create_clicks]
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
        animation_frame = parameter[SCATTER_MAP_CONSTANT[FRAME]],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter[SCATTER_MAP_CONSTANT[MESSAGE]]
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig


def create_scatter_geo(create_clicks, parameter):
    data = collection.data[create_clicks]
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
        animation_frame = parameter[SCATTER_GEO_CONSTANT[FRAME]],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter[SCATTER_GEO_CONSTANT[MESSAGE]],
        projection = "natural earth"
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig


def create_bar_chart_race(create_clicks, parameter):
    data = collection.data[create_clicks]

    race_plot = barplot(
        data,
        item_column = parameter[BAR_CHART_RACE_CONSTANT[ITEM]],
        value_column = parameter[BAR_CHART_RACE_CONSTANT[VALUE]],
        time_column = parameter[BAR_CHART_RACE_CONSTANT[FRAME]]
    )
    fig = race_plot.plot(title = 'Top 10 Crops from 1961 to 2018',
                             item_label = 'Top 10 crops',
                             value_label = 'Production quantity (tonnes)',
                             frame_duration = 800)
    configure_fig(fig)
    return fig


def create_density(create_clicks, parameter):
    data = collection.data[create_clicks]
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
        radius = 10,
        center = dict(lat = 0, lon = 180),
        zoom = 0,
        animation_frame = parameter[DENSITY_CONSTANT[FRAME]],
        mapbox_style = "stamen-terrain")

    configure_fig(fig)
    return fig


def create_choropleth(create_clicks,parameter):
    data = collection.data[create_clicks]
    fig = px.choropleth(
        data, locations = parameter[CHOROPLETH_CONSTANT[LOCATIONS]],
        color = parameter[CHOROPLETH_CONSTANT[COLOR]],
        hover_name = parameter[CHOROPLETH_CONSTANT[NAME]],
        animation_frame = parameter[CHOROPLETH_CONSTANT[FRAME]],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter[CHOROPLETH_CONSTANT[MESSAGE]],
        color_continuous_scale=px.colors.sequential.Plasma,
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig

def create_visualization(screen_width, create_clicks, ftype, param, maxValue, df_date):
    return html.Div(
                    style={'width': screen_width/2.2, 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
                    children=html.Div([
                        dcc.Store(id={'type': 'is-animating', 'index': create_clicks}, data = False),
                        dcc.Store(id='uuid', data = create_clicks),
                        dcc.Store(id={'type': 'figure-type', 'index': create_clicks}, data = ftype),
                        dcc.Store(id={'type': 'my_param', 'index': create_clicks}, data=param),
                        dcc.Interval(
                            id={'type': 'interval', 'index': create_clicks},
                            interval=200,
                            n_intervals=0,
                            max_intervals=maxValue,
                            disabled=True
                        ),
                        dcc.Graph(id={'type': 'visualization', 'index': create_clicks}, figure=create_figure(create_clicks, param, ftype)),
                        dcc.Slider(
                            id={'type': 'anim-slider', 'index': create_clicks},
                            updatemode='drag',
                            min=0,
                            max=maxValue,
                            value=0,
                            marks={str(i): str(des) for i, des in
                                   zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
                        ),
                        html.Div([
                            html.Button('play', id={'type': 'play-btn', 'index': create_clicks}),
                            html.Label(df_date[0], id={'type': 'slider-label', 'index': create_clicks})
                        ]),
                        html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks}, style={'position':'absolute', 'top':0}),
                    ]),
                )