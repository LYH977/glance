
import plotly.express as px

from components.visual.figures.configuration import configure_fig
from utils.constant import CHOROPLETH_CONSTANT, LOCATIONS, COLOR, NAME, FRAME, MESSAGE


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