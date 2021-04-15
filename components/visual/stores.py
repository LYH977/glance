
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils import collection
from utils.constant import TIME
from utils.method import get_last_timestamp


def stores_markup(create_clicks, param, figure, tformat,  initial_frame, dbname, now,  new_col):
    last_nano = get_last_timestamp(collection.temp[TIME])
    total_rows = len(collection.data[create_clicks].index)
    return html.Div([
        dcc.Store(id = {'type': 'my-index', 'index': create_clicks}, data = create_clicks),
        dcc.Store(id = {'type': 'is-animating', 'index': create_clicks}, data = False),
        dcc.Store(id = {'type': 'my_param', 'index': create_clicks}, data = param),
        dcc.Store(id = {'type': 'back-buffer', 'index': create_clicks}, data = figure),
        dcc.Store(id = {'type': 'frame-format', 'index': create_clicks}, data = tformat),
        dcc.Store(id = {'type': 'last-timestamp', 'index': create_clicks}, data = last_nano),
        dcc.Store(id = {'type': 'at-max', 'index': create_clicks}, data = False),
        dcc.Store(id = {'type': 'last-notif-click', 'index': create_clicks}, data = ''),
        dcc.Store(id = {'type': 'celery-data', 'index': create_clicks}, data = None),
        dcc.Store(id = {'type': 'current-frame', 'index': create_clicks}, data =  initial_frame),
        dcc.Store(id = {'type': 'db-name', 'index': create_clicks}, data = dbname),
        dcc.Store(id = {'type': 'redis-timestamp', 'index': create_clicks}, data = now),
        dcc.Store(id = {'type': 'last-total-rows', 'index': create_clicks}, data = total_rows),
        dcc.Store(id = {'type': 'is-slided-up', 'index': create_clicks}, data = False),
        dcc.Store(id = {'type': 'new-column-info', 'index': create_clicks}, data = new_col),
        dcc.Store(id= {'type': 'export-name', 'index': create_clicks}, data = None),
        # dcc.Store(id={'type': 'max-frame', 'index': create_clicks}, data = max_frame),

    ])
