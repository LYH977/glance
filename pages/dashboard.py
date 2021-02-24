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
from raceplotly.plots import barplot


df = px.data.gapminder()
fig = px.choropleth(df, locations="iso_alpha",
                    color="lifeExp", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma, animation_frame='year')

# print(fig)
layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div(id='visual-container', children=[]), width="auto", style={'background':'green'})  ,
        dbc.Col(upload_modal.modal,style={'background':'yellow'}),

    ])
    ,dcc.Graph(id='temporary',    figure=fig)
, ])


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
