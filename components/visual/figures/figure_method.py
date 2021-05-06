from components.visual.figures.bar_chart_race import create_bar_chart_race
from components.visual.figures.choropleth import create_choropleth
from components.visual.figures.density import create_density
from components.visual.figures.scatter import create_scattermap
from utils.constant import SCATTER_MAP,  BAR_CHART_RACE, DENSITY, CHOROPLETH


def create_figure(data, parameter, ftype):
    if ftype == SCATTER_MAP:
        return create_scattermap(data,parameter)
    # elif ftype == SCATTER_GEO:
    #     return create_scatter_geo(data,parameter)
    elif ftype == BAR_CHART_RACE:
        return create_bar_chart_race(data, parameter)
    elif ftype == DENSITY:
        return create_density(data, parameter)
    elif ftype == CHOROPLETH:
        return create_choropleth(data, parameter)




