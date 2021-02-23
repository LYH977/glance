import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from app import app
from components import visualization, upload_modal
from utils import collection
from utils.method import  set_slider_calendar

# from callback import upload_modal_callback
# from database import dbConfig

import plotly.express as px
import pandas as pd



# data = visualization.data
# data2 = visualization.data2
# df_date = data['Date'].unique()
# maxValue = df_date.shape[0] - 1
# df = px.data.gapminder()
# print(df.head(10))
# df.to_csv("output.csv")
# fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
#                      hover_name="country", size="pop",
#                      animation_frame="year",
#                      projection="natural earth")

layout = html.Div(
    dbc.Row([
        dbc.Col(html.Div(id='visual-container', children=[]), width="auto", style={'background':'green'})  ,
        dbc.Col(upload_modal.modal,style={'background':'yellow'}),
        # dcc.Graph(id='temporary',    figure=fig)
    ])

, )


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
