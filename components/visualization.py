import pandas as pd                  # for DataFrames
import plotly.express as px
import dash_core_components as dcc
import os
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE, \
    SCATTER_MAP_CONSTANT, LATITUDE, LONGITUDE, SIZE, COLOR, NAME, FRAME, MESSAGE, SCATTER_GEO_CONSTANT, \
    BAR_CHART_RACE_CONSTANT, ITEM, VALUE, DENSITY_CONSTANT, Z, CHOROPLETH_CONSTANT, LOCATIONS
from raceplotly.plots import barplot

access_token = os.environ['MAP_TOKEN']
px.set_mapbox_access_token(access_token)

# data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
# data = pd.read_csv(data_url)

def create_visualization(dataframe, parameter, ftype):
    if ftype == SCATTER_MAP:
        return create_scattermap(dataframe,parameter)
    elif ftype == SCATTER_GEO:
        return create_scatter_geo(dataframe,parameter)
    elif ftype == BAR_CHART_RACE:
        return create_bar_chart_race(dataframe, parameter)
    elif ftype == DENSITY:
        return create_density(dataframe, parameter)
    elif ftype == CHOROPLETH:
        return create_choropleth(dataframe, parameter)



def configure_fig(fig):
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
    fig.layout.coloraxis.showscale = False
    fig.layout.margin.t = 30
    fig.layout.margin.b = 30
    fig.layout.updatemenus[0].showactive = True



def create_scattermap(dataframe,parameter):
    data = dataframe.dropna()
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


def create_scatter_geo(dataframe,parameter):
    data = dataframe.dropna()
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


def create_bar_chart_race(dataframe,parameter):
    data = dataframe.dropna()
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


def create_density(dataframe,parameter):
    data = dataframe.dropna()
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


def create_choropleth(dataframe,parameter):
    data = dataframe.dropna()
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