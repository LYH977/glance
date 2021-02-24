import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate
import tkinter as tk

from components import visualization, upload_modal
from utils import collection
from utils.method import  set_slider_calendar

root = tk.Tk()
screen_width = root.winfo_screenwidth()

def render_container(create_clicks, param, ftype):
    data = collection.temp.dropna()
    df_date = data[param['frame']].unique()
    maxValue = df_date.shape[0] - 1
    print('create_clicks',create_clicks)
    return html.Div(
                    style={'width': screen_width/2.2, 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
                    children=html.Div([
                        dcc.Store(id={'type': 'is-animating', 'index': create_clicks}, data = False),
                        dcc.Store(id='uuid', data = create_clicks),
                        dcc.Store(id={'type': 'figure-type', 'index': create_clicks}, data = ftype),
                        dcc.Store(id={'type': 'my_param', 'index': create_clicks}, data=param),
                        dcc.Interval(
                            id={'type': 'interval', 'index': create_clicks},
                            interval=200,
                            n_intervals=0,
                            max_intervals=maxValue,
                            disabled=True
                        ),
                        dcc.Graph(id={'type': 'visualization', 'index': create_clicks}, figure=visualization.create_visualization(collection.temp, param, ftype)),
                        dcc.Slider(
                            id={'type': 'anim-slider', 'index': create_clicks},
                            updatemode='drag',
                            min=0,
                            max=maxValue,
                            value=0,
                            marks={str(i): str(des) for i, des in
                                   zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
                        ),
                        html.Div([
                            html.Button('play', id={'type': 'play-btn', 'index': create_clicks}),
                            html.Label(df_date[0], id={'type': 'slider-label', 'index': create_clicks})
                        ]),
                        html.Button('Delete', id={'type': 'dlt-btn', 'index': create_clicks}, style={'position':'absolute', 'top':0}),
                    ]),
                )