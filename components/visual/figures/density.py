import plotly.express as px

from components.visual.figures.configuration import configure_fig, convert_to_float
from utils.constant import DENSITY_CONSTANT, LATITUDE, LONGITUDE, Z, MESSAGE, FRAME, DENSITY


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
        color_continuous_scale=px.colors.sequential.Pinkyl,
        zoom = 0,
        animation_frame = FRAME,
        mapbox_style = "dark",
        # height= 200

    )
    configure_fig(fig, DENSITY)
    return fig