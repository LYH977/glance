
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

def intervals_markup(create_clicks, maxValue):
    return html.Div([
        dcc.Interval(
            id = {'type': 'interval', 'index': create_clicks},
            interval = 200,
            n_intervals = 0,
            max_intervals = maxValue,
            disabled = True
        ),
        dcc.Interval(
            id = {'type': 'live-interval', 'index': create_clicks},
            interval = 2000,
            n_intervals = 0,
            disabled = True
        ),
        dcc.Interval(
            id = {'type': 'celery-interval', 'index': create_clicks},
            interval = 2000,
            n_intervals = 0,
        ),
        dcc.Interval(
            id = {'type': 'export-interval', 'index': create_clicks},
            interval  =  1000,
            n_intervals  =  0,
            disabled  =  True
        ),


    ])