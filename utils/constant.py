import os
from geopy.geocoders import MapBox

NANOSECOND = 1000000000.0
DAY = '%d'
MONTH = '%m'
YEAR = '%Y'
HOUR = '%H'
MINUTE = '%M'
SECOND = '%S'
MILLISEC = '%f'
STANDARD_T_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT = {
    'YEAR': YEAR,
    'MONTH': MONTH,
    'DAY': DAY,
    'HOUR': HOUR,
    'MINUTE': MINUTE,
    'SECOND': SECOND,
    'YEAR-MONTH': '{}-{}'.format(YEAR, MONTH),
    'YEAR-MONTH-DAY': '{}-{}-{}'.format(YEAR, MONTH,DAY),
    'HOUR:MINUTE:SECOND': '{}:{}:{}'.format(HOUR, MINUTE, SECOND),
    'YEAR-MONTH-DAY, HOUR:MINUTE:SECOND': '{}-{}-{}, {}:{}:{}'.format(YEAR, MONTH, DAY, HOUR, MINUTE, SECOND),
}
TIME = 'time'
TAG = 'TAG'
FIELD = 'FIELD'

SCATTER_MAP = 'Scatter Map'
# SCATTER_GEO = 'Scatter Geo'
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

MAXIMUM = 'MAXIMUM'
MINIMUM = 'MINIMUM'

CREATE_BTN_ID = {
    SCATTER_MAP: SM_PARAM,
    # SCATTER_GEO: SG_PARAM,
    BAR_CHART_RACE: BC_PARAM,
    DENSITY: D_PARAM,
    CHOROPLETH: CH_PARAM,
    CAROUSEL: CA_PARAM,
}

FIGURE_OPTION = [
    SCATTER_MAP,
    # SCATTER_GEO,
    BAR_CHART_RACE,
    DENSITY,
    CHOROPLETH,
    CAROUSEL
]


SCATTER_MAP_CONSTANT = {
    LATITUDE : 'sm_latitude',
    LONGITUDE: 'sm_longitude',
    SIZE: 'sm_size',
    COLOR: 'sm_color',
    NAME: 'sm_name',
    MESSAGE: 'sm_message',
}



# SCATTER_GEO_CONSTANT = {
#     LATITUDE : 'sg_latitude',
#     LONGITUDE: 'sg_longitude',
#     SIZE: 'sg_size',
#     COLOR: 'sg_color',
#     NAME: 'sg_name',
#     MESSAGE: 'sg_message',
# }



BAR_CHART_RACE_CONSTANT = {
    ITEM : 'bc_item',
    VALUE : 'bc_value',
}



DENSITY_CONSTANT = {
    LATITUDE : 'd_latitude',
    LONGITUDE: 'd_longitude',
    Z: 'd_z',
    MESSAGE: 'd_message',
}



CHOROPLETH_CONSTANT = {
    LOCATIONS : 'ch_locations',
    COLOR: 'ch_color',
    NAME: 'ch_name',
    MESSAGE: 'ch_message',
}


CAROUSEL_CONSTANT = {
    ITEM : 'ca_item',
}

SCATTER_MAP_PARAM = {
    SCATTER_MAP_CONSTANT[LATITUDE]: { 'label':'Latitude*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[LONGITUDE]: { 'label':'Longitude*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[SIZE]: { 'label':'Size*', 'value': None, 'multi': False },
    SCATTER_MAP_CONSTANT[COLOR]: { 'label':'Color*', 'value': None, 'multi': False },
    SCATTER_MAP_CONSTANT[NAME]: { 'label':'Name*', 'value': None , 'multi': False},
    SCATTER_MAP_CONSTANT[MESSAGE]: { 'label':'Additional Message', 'value': [] , 'multi': True},
}

# SCATTER_GEO_PARAM = {
#     SCATTER_GEO_CONSTANT[LATITUDE]: { 'label':'Latitude*', 'value': None , 'multi': False},
#     SCATTER_GEO_CONSTANT[LONGITUDE]: { 'label':'Longitude*', 'value': None , 'multi': False},
#     SCATTER_GEO_CONSTANT[SIZE]: { 'label':'Size*', 'value': None, 'multi': False },
#     SCATTER_GEO_CONSTANT[COLOR]: { 'label':'Color*', 'value': None, 'multi': False },
#     SCATTER_GEO_CONSTANT[NAME]: { 'label':'Name*', 'value': None , 'multi': False},
#     SCATTER_GEO_CONSTANT[MESSAGE]: { 'label':'Additional Message', 'value': [] , 'multi': True},
# }

BAR_CHART_RACE_PARAM = {
    BAR_CHART_RACE_CONSTANT[ITEM] : { 'label':'Item*', 'value': None , 'multi': False},
    BAR_CHART_RACE_CONSTANT[VALUE] : { 'label':'Value*', 'value': None , 'multi': False},

}

DENSITY_PARAM = {
    DENSITY_CONSTANT[LATITUDE] : { 'label':'Latitude*', 'value': None , 'multi': False},
    DENSITY_CONSTANT[LONGITUDE] : { 'label':'Longitude*', 'value': None , 'multi': False},
    DENSITY_CONSTANT[Z] : {'label': 'Magnitude*', 'value': None, 'multi': False},
    DENSITY_CONSTANT[MESSAGE] : { 'label':'Additional Message', 'value': [] , 'multi': True},

}

CHOROPLETH_PARAM = {
    CHOROPLETH_CONSTANT[LOCATIONS] : { 'label':'Locations*', 'value': None , 'multi': False},
    CHOROPLETH_CONSTANT[COLOR] : { 'label':'Color*', 'value': None , 'multi': False},
    CHOROPLETH_CONSTANT[NAME] : {'label': 'Name*', 'value': None, 'multi': False},
    CHOROPLETH_CONSTANT[MESSAGE] : {'label': 'Additional Message', 'value': [], 'multi': True},

}

CAROUSEL_PARAM = {
    CAROUSEL_CONSTANT[ITEM] : { 'label':'Item*', 'value': None , 'multi': False},

}

FIGURE_PARAM = {
    SCATTER_MAP : SCATTER_MAP_PARAM,
    # SCATTER_GEO : SCATTER_GEO_PARAM,
    BAR_CHART_RACE : BAR_CHART_RACE_PARAM,
    DENSITY : DENSITY_PARAM,
    CHOROPLETH : CHOROPLETH_PARAM,
    CAROUSEL:CAROUSEL_PARAM,
}
# -------------------------------------------------------------------------

SCATTER_MAP_NOTIF = {
    TAG: [  SCATTER_MAP_CONSTANT[LATITUDE], SCATTER_MAP_CONSTANT[LONGITUDE], SCATTER_MAP_CONSTANT[NAME]  ],
    FIELD: [ SCATTER_MAP_CONSTANT[SIZE], SCATTER_MAP_CONSTANT[COLOR] ]
}

# SCATTER_GEO_NOTIF = {
#     TAG: [  SCATTER_GEO_CONSTANT[LATITUDE], SCATTER_GEO_CONSTANT[LONGITUDE], SCATTER_GEO_CONSTANT[NAME]  ],
#     FIELD: [ SCATTER_GEO_CONSTANT[SIZE], SCATTER_GEO_CONSTANT[COLOR] ]
# }

BAR_CHART_RACE_NOTIF = {
    TAG: [BAR_CHART_RACE_CONSTANT[ITEM]],
    FIELD: [BAR_CHART_RACE_CONSTANT[VALUE]]
}

DENSITY_NOTIF = {
    TAG: [  DENSITY_CONSTANT[LATITUDE], DENSITY_CONSTANT[LONGITUDE]  ],
    FIELD: [ DENSITY_CONSTANT[Z] ]
}


CHOROPLETH_NOTIF = {
    TAG: [  CHOROPLETH_CONSTANT[LOCATIONS], CHOROPLETH_CONSTANT[NAME]  ],
    FIELD: [ CHOROPLETH_CONSTANT[COLOR] ]
}

CAROUSEL_NOTIF = {
    TAG: [ ],
    FIELD: [ CAROUSEL_CONSTANT[ITEM] ]
}

NOTIFICATION_PARAM = {
    SCATTER_MAP: SCATTER_MAP_NOTIF,
    # SCATTER_GEO: SCATTER_GEO_NOTIF,
    BAR_CHART_RACE: BAR_CHART_RACE_NOTIF,
    DENSITY: DENSITY_NOTIF,
    CHOROPLETH: CHOROPLETH_NOTIF,
    CAROUSEL: CAROUSEL_NOTIF,
}

COLLAPSE_HEIGHT = 150
VISUAL_HEIGHT = 300

MAPBOX_TYPES = [ 'streets',  'light', 'dark', 'satellite-streets']

SEQUENTIAL_COLOR = [
'Aggrnyl' ,'Agsunset',
 'Blackbody' ,  'Bluered', 'Blues',   'Blugrn',  'Bluyl',   'Brwnyl', 'BuGn','BuPu','Burg','Burgyl',
'Cividis',
'Darkmint',
 'Electric','Emrld',
'GnBu','Greens',  'Greys',
 'Hot',
'Inferno',
'Jet',
'Magenta', 'Magma', 'Mint',
'OrRd','Oranges', 'Oryel',
'Peach',   'Pinkyl',  'Plasma',  'Plotly3', 'PuBu','PuBuGn',  'PuRd','Purp','Purples', 'Purpor',
'Rainbow', 'RdBu', 'RdPu','Redor',   'Reds',
'Sunset',  'Sunsetdark',
 'Teal','Tealgrn', 'Turbo',
'Viridis',
'YlGn','YlGnBu',  'YlorBr',  'YlorRd',
'algae',   'amp',
'deep', 'dense',
 'gray',
'haline',
'ice',
'matter',
'solar',   'speed',
'tempo','thermal', 'turbid',

]

MAPBOX_GEOCODER = MapBox(os.environ['MAP_TOKEN'])