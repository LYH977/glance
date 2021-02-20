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

def render_container(add_clicks,param, uuid):
    data = collection.data.dropna()
    df_date = data[param['frame']].unique()
    maxValue = df_date.shape[0] - 1
    return html.Div(
                    style={'width': screen_width/2, 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
                    children=html.Div([
                        dcc.Store(id='is-animating', data=False),
                        dcc.Store(id='uuid', data=uuid),
                        dcc.Interval(
                            id='interval',
                            interval=200,
                            n_intervals=0,
                            max_intervals=maxValue,
                            disabled=True
                        ),
                        dcc.Graph(id={'type': 'visualization', 'index': add_clicks}, figure=visualization.create_scattermap(collection.data, param)),
                        dcc.Slider(
                            id='anim-slider',
                            updatemode='drag',
                            min=0,
                            max=maxValue,
                            value=0,
                            marks={str(i): str(des) for i, des in
                                   zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
                        ),
                        html.Div([
                            html.Button('play', id='play-btn'),
                            html.Label(df_date[0], id='slider-label')
                        ]),
                        html.Button('Delete', id={'type': 'dlt-btn', 'index': add_clicks}, style={'position':'absolute', 'top':0}),
                    ]),
                )