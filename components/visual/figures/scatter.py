import plotly.express as px

from components.visual.figures.configuration import convert_to_float, configure_fig
from utils.constant import SCATTER_MAP_CONSTANT, LATITUDE, LONGITUDE, SIZE, COLOR, NAME, FRAME, MESSAGE, \
     SCATTER_MAP


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
    configure_fig(fig, SCATTER_MAP)
    return fig


# def create_scatter_geo(data, parameter):
#     convert_to_float(data, parameter, [
#         SCATTER_GEO_CONSTANT[LATITUDE],
#         SCATTER_GEO_CONSTANT[LONGITUDE]
#     ])
#     fig = px.scatter_geo(
#         data, lat = parameter[ SCATTER_GEO_CONSTANT[LATITUDE] ] ,
#         lon = parameter[SCATTER_GEO_CONSTANT[LONGITUDE]],
#         size = parameter[SCATTER_GEO_CONSTANT[SIZE]],
#         color = parameter[SCATTER_GEO_CONSTANT[COLOR]],
#         hover_name = parameter[SCATTER_GEO_CONSTANT[NAME]],
#         animation_frame = FRAME,
#         hover_data = parameter[SCATTER_GEO_CONSTANT[MESSAGE]],
#         projection = "natural earth"
#     )
#     configure_fig(fig)
#     return fig