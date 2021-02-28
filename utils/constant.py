NANOSECOND = 1000000000.0
DAY = '%d'
MONTH = '%m'
YEAR = '%Y'
HOUR = '%H'
MINUTE = '%M'
SECOND = '%S'
MILLISEC = '%f'

'20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f'

SCATTER_MAP = 'Scatter Map'
SCATTER_GEO = 'Scatter Geo'
BAR_CHART_RACE = 'Bar Chart Race'
DENSITY = 'Density'
CHOROPLETH = 'Choropleth'
CAROUSEL = 'Carousel'

SM_PARAM = 'sm-cid'
SG_PARAM = 'sg-cid'
BC_PARAM = 'bc-cid'
D_PARAM = 'd-cid'
CH_PARAM = 'ch-cid'
CA_PARAM = 'ca-cid'

LATITUDE = 'latitude'
LONGITUDE = 'longitude'
SIZE = 'size'
COLOR = 'color'
NAME = 'name'
MESSAGE = 'message'
FRAME = 'frame'
ITEM = 'item'
VALUE = 'value'
Z = 'z'
LOCATIONS = 'lcoations'

CREATE_BTN_ID = {
    SCATTER_MAP: SM_PARAM,
    SCATTER_GEO: SG_PARAM,
    BAR_CHART_RACE: BC_PARAM,
    DENSITY: D_PARAM,
    CHOROPLETH: CH_PARAM,
    CAROUSEL: CA_PARAM,
}

FIGURE_OPTION = [
    SCATTER_MAP,
    SCATTER_GEO,
    BAR_CHART_RACE,
    DENSITY,
    CHOROPLETH,
    CAROUSEL
]

FRAME_NAME = {
    SCATTER_MAP :'sm_frame',
    SCATTER_GEO: 'sg_frame',
    BAR_CHART_RACE: 'bc_frame',
    DENSITY: 'd_frame',
    CHOROPLETH: 'ch_frame',
    CAROUSEL: 'ca_frame',

}

SCATTER_MAP_CONSTANT = {
    LATITUDE : 'sm_latitude',
    LONGITUDE: 'sm_longitude',
    SIZE: 'sm_size',
    COLOR: 'sm_color',
    NAME: 'sm_name',
    FRAME: FRAME_NAME[SCATTER_MAP],
    MESSAGE: 'sm_message',
}

SCATTER_GEO_CONSTANT = {
    LATITUDE : 'sg_latitude',
    LONGITUDE: 'sg_longitude',
    SIZE: 'sg_size',
    COLOR: 'sg_color',
    NAME: 'sg_name',
    FRAME: FRAME_NAME[SCATTER_GEO],
    MESSAGE: 'sg_message',
}

BAR_CHART_RACE_CONSTANT = {
    ITEM : 'bc_item',
    VALUE : 'bc_value',
    FRAME : FRAME_NAME[BAR_CHART_RACE],
}

DENSITY_CONSTANT = {
    LATITUDE : 'd_latitude',
    LONGITUDE: 'd_longitude',
    Z: 'd_z',
    FRAME: FRAME_NAME[DENSITY],
    MESSAGE: 'd_message',
}

CHOROPLETH_CONSTANT = {
    LOCATIONS : 'ch_locations',
    COLOR: 'ch_color',
    NAME: 'ch_name',
    FRAME: FRAME_NAME[CHOROPLETH],
    MESSAGE: 'ch_message',
}

CAROUSEL_CONSTANT = {
    ITEM : 'ca_item',
    FRAME: FRAME_NAME[CAROUSEL],
}

SCATTER_MAP_PARAM = {
    SCATTER_MAP_CONSTANT[LATITUDE]: { 'label':'Latitude*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[LONGITUDE]: { 'label':'Longitude*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[SIZE]: { 'label':'Size*', 'value': None, 'multi': False },
    SCATTER_MAP_CONSTANT[COLOR]: { 'label':'Color*', 'value': None, 'multi': False },
    SCATTER_MAP_CONSTANT[NAME]: { 'label':'Name*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[FRAME] : { 'label':'Animation Frame*', 'value': None, 'multi': False },
    SCATTER_MAP_CONSTANT[MESSAGE]: { 'label':'Additional Message', 'value': [] , 'multi': True},
}

SCATTER_GEO_PARAM = {
    SCATTER_GEO_CONSTANT[LATITUDE]: { 'label':'Latitude*', 'value': None , 'multi': False},
    SCATTER_GEO_CONSTANT[LONGITUDE]: { 'label':'Longitude*', 'value': None , 'multi': False},
    SCATTER_GEO_CONSTANT[SIZE]: { 'label':'Size*', 'value': None, 'multi': False },
    SCATTER_GEO_CONSTANT[COLOR]: { 'label':'Color*', 'value': None, 'multi': False },
    SCATTER_GEO_CONSTANT[NAME]: { 'label':'Name*', 'value': None , 'multi': False},
    SCATTER_GEO_CONSTANT[FRAME] : { 'label':'Animation Frame*', 'value': None, 'multi': False },
    SCATTER_GEO_CONSTANT[MESSAGE]: { 'label':'Additional Message', 'value': [] , 'multi': True},
}

BAR_CHART_RACE_PARAM = {
    BAR_CHART_RACE_CONSTANT[ITEM] : { 'label':'Item*', 'value': None , 'multi': False},
    BAR_CHART_RACE_CONSTANT[VALUE] : { 'label':'Value*', 'value': None , 'multi': False},
    BAR_CHART_RACE_CONSTANT[FRAME] : { 'label':'Time*', 'value': None, 'multi': False },

}

DENSITY_PARAM = {
    DENSITY_CONSTANT[LATITUDE] : { 'label':'Latitude*', 'value': None , 'multi': False},
    DENSITY_CONSTANT[LONGITUDE] : { 'label':'Longitude*', 'value': None , 'multi': False},
    DENSITY_CONSTANT[Z] : {'label': 'Magnitude*', 'value': None, 'multi': False},
    DENSITY_CONSTANT[FRAME] : {'label': 'Time*', 'value': None, 'multi': False},
    DENSITY_CONSTANT[MESSAGE] : { 'label':'Additional Message', 'value': [] , 'multi': True},

}

CHOROPLETH_PARAM = {
    CHOROPLETH_CONSTANT[LOCATIONS] : { 'label':'Locations*', 'value': None , 'multi': False},
    CHOROPLETH_CONSTANT[COLOR] : { 'label':'Color*', 'value': None , 'multi': False},
    CHOROPLETH_CONSTANT[NAME] : {'label': 'Name*', 'value': None, 'multi': False},
    CHOROPLETH_CONSTANT[FRAME] : { 'label':'Frame*', 'value': None, 'multi': False },
    CHOROPLETH_CONSTANT[MESSAGE] : {'label': 'Additional Message', 'value': [], 'multi': True},

}

CAROUSEL_PARAM = {
    CAROUSEL_CONSTANT[ITEM] : { 'label':'Item*', 'value': None , 'multi': False},
    CAROUSEL_CONSTANT[FRAME] : { 'label':'Time*', 'value': None, 'multi': False },

}

FIGURE_PARAM = {
    SCATTER_MAP : SCATTER_MAP_PARAM,
    SCATTER_GEO : SCATTER_GEO_PARAM,
    BAR_CHART_RACE : BAR_CHART_RACE_PARAM,
    DENSITY : DENSITY_PARAM,
    CHOROPLETH : CHOROPLETH_PARAM,
    CAROUSEL:CAROUSEL_PARAM,
}