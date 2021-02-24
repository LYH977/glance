
SCATTER_MAP = 'Scatter Map'
SCATTER_GEO = 'Scatter Geo'
BAR_CHART_RACE = 'Bar Chart Race'
DENSITY = 'Density'
CHOROPLETH = 'Choropleth'
CAROUSEL = 'Carousel'

FIGURE_OPTION = [
    SCATTER_MAP,
    SCATTER_GEO,
    BAR_CHART_RACE,
    DENSITY,
    CHOROPLETH,
    CAROUSEL
]

SCATTER_MAP_PARAM = {
    'latitude': { 'label':'Latitude*', 'value': None , 'multi': False},
    'longitude': { 'label':'Longitude*', 'value': None , 'multi': False},
    'size': { 'label':'Size*', 'value': None, 'multi': False },
    'color': { 'label':'Color*', 'value': None, 'multi': False },
    'name': { 'label':'Name*', 'value': None , 'multi': False},
    'frame': { 'label':'Animation Frame*', 'value': None, 'multi': False },
    'message': { 'label':'Additional Message', 'value': [] , 'multi': True},
}

SCATTER_GEO_PARAM = {
    'latitude': { 'label':'Latitude*', 'value': None , 'multi': False},
    'longitude': { 'label':'Longitude*', 'value': None , 'multi': False},
    'size': { 'label':'Size*', 'value': None, 'multi': False },
    'color': { 'label':'Color*', 'value': None, 'multi': False },
    'name': { 'label':'Name*', 'value': None , 'multi': False},
    'frame': { 'label':'Animation Frame*', 'value': None, 'multi': False },
    'message': { 'label':'Additional Message', 'value': [] , 'multi': True},
}

BAR_CHART_RACE_PARAM = {
    'item': { 'label':'Item*', 'value': None , 'multi': False},
    'value': { 'label':'Value*', 'value': None , 'multi': False},
    'frame': { 'label':'Time*', 'value': None, 'multi': False },

}

DENSITY_PARAM = {
    'latitude': { 'label':'Latitude*', 'value': None , 'multi': False},
    'longitude': { 'label':'Longitude*', 'value': None , 'multi': False},
    'z': {'label': 'Magnitude*', 'value': None, 'multi': False},
    'frame': {'label': 'Time*', 'value': None, 'multi': False},
    'message': { 'label':'Additional Message', 'value': [] , 'multi': True},

}

CHOROPLETH_PARAM = {
    'locations': { 'label':'Locations*', 'value': None , 'multi': False},
    'color': { 'label':'Color*', 'value': None , 'multi': False},
    'name': {'label': 'Name*', 'value': None, 'multi': False},
    'frame': { 'label':'Frame*', 'value': None, 'multi': False },
    'message': {'label': 'Additional Message', 'value': [], 'multi': True},

}

CAROUSEL_PARAM = {
    'item': { 'label':'Item*', 'value': None , 'multi': False},
    'value': { 'label':'Value*', 'value': None , 'multi': False},
    'frame': { 'label':'Time*', 'value': None, 'multi': False },

}

FIGURE_PARAM = {
    SCATTER_MAP : SCATTER_MAP_PARAM,
    SCATTER_GEO : SCATTER_GEO_PARAM,
    BAR_CHART_RACE : BAR_CHART_RACE_PARAM,
    DENSITY : DENSITY_PARAM,
    CHOROPLETH : CHOROPLETH_PARAM,
    CAROUSEL:CAROUSEL_PARAM,
}