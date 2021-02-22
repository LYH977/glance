

SCATTER_MAP_PARAM = {
    'latitude': { 'label':'Latitude*', 'value': None , 'multi': False},
    'longitude': { 'label':'Longitude*', 'value': None , 'multi': False},
    'size': { 'label':'Size*', 'value': None, 'multi': False },
    'color': { 'label':'Color*', 'value': None, 'multi': False },
    'name': { 'label':'Name*', 'value': None , 'multi': False},
    'frame': { 'label':'Animation Frame*', 'value': None, 'multi': False },
    'message': { 'label':'Additional Message', 'value': [] , 'multi': False},
}


FIGURE_OPTION = [
    'Scatter Map',
    'Scatter Geo',
    'Bar Chart Race',
    'Density',
    'Choropleth',
    'Carousel'
]

FIGURE_PARAM = {
    'Scatter Map' : SCATTER_MAP_PARAM,
    'Scatter Geo' : 'Scatter Geo',
    'Bar Chart Race' : 'Bar Chart Race',
    'Density' : 'Density',
    'Choropleth' : 'Choropleth',
    'Carousel' :'Carousel',
}