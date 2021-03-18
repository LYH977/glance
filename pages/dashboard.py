import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate

from app import app
from components import visualization, select_dataset_modal
from utils import collection
from utils.method import  set_slider_calendar

# from callback import upload_modal_callback
# from database import dbConfig

import plotly.express as px
import pandas as pd
from raceplotly.plots import barplot


layout = html.Div([
    html.Div('it is empty', id='empty-scene', className='empty-scene'),
    html.Div(id = 'visual-container', children=[], style={
    'display': 'grid',
    'grid-template-columns': '1fr 1fr',

    }),
    select_dataset_modal.modal
, ], style={
    'position':'relative',
    # 'background':'#242444'
    }
)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
