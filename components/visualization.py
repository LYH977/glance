import pandas as pd                  # for DataFrames
import plotly.express as px
import dash_core_components as dcc
import os
from utils.constant import SCATTER_MAP, SCATTER_GEO, DENSITY, CAROUSEL, CHOROPLETH, BAR_CHART_RACE
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
    print(px.data.gapminder().columns)
    data = dataframe.dropna()
    fig = px.scatter_mapbox(
        data, lat = parameter['latitude'], lon = parameter['longitude'],
        size = parameter['size'], size_max = 50,
        color = parameter['color'], color_continuous_scale = px.colors.sequential.Pinkyl,
        hover_name = parameter['name'],
        mapbox_style = 'dark', zoom=1,
        animation_frame = parameter['frame'],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter['message']
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig


def create_scatter_geo(dataframe,parameter):
    data = dataframe.dropna()
    fig = px.scatter_geo(
        data, lat = parameter['latitude'], lon = parameter['longitude'],
        size = parameter['size'],
        color = parameter['color'],
        hover_name = parameter['name'],
        animation_frame = parameter['frame'],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter['message'],
        projection = "natural earth"
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    configure_fig(fig)
    return fig


def create_bar_chart_race(dataframe,parameter):
    data = dataframe.dropna()
    race_plot = barplot(data, item_column = parameter['item'],  value_column = parameter['value'],  time_column = parameter['frame'])
    fig = race_plot.plot(title = 'Top 10 Crops from 1961 to 2018',
                             item_label = 'Top 10 crops',
                             value_label = 'Production quantity (tonnes)',
                             frame_duration = 800)
    configure_fig(fig)
    return fig


def create_density(dataframe,parameter):
    data = dataframe.dropna()
    fig = px.density_mapbox(data, lat = parameter['latitude'], lon = parameter['longitude'], z = parameter['z'], radius = 10,
                            center = dict(lat = 0, lon = 180), zoom = 0, animation_frame = parameter['frame'],
                            mapbox_style = "stamen-terrain")

    configure_fig(fig)
    return fig


def create_choropleth(dataframe,parameter):
    data = dataframe.dropna()
    fig = px.choropleth(
        data, locations = parameter['locations'],
        color = parameter['color'],
        hover_name = parameter['name'],
        animation_frame = parameter['frame'],
        # animation_group="Province/State",
        height = 600,
        hover_data = parameter['message'],
        color_continuous_scale=px.colors.sequential.Plasma,
        # hover_data=['Active', 'Confirmed']
        # custom_data=['Date']
    )
    print(fig)
    configure_fig(fig)
    return fig