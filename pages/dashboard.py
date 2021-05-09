import dash_html_components as html
import os
import plotly.graph_objects as go

from components import select_dataset_modal
import plotly.express as px
import dash_core_components as dcc
import tkinter as tk
from geopy.geocoders import MapBox
# from callback import upload_modal_callback
# from database import dbConfig
# px.colors.sequential.

# print('pltlys scale', px.colors.sequential.a )
# print('sequential ', px.colors.PLOTLY_SCALES.keys() )
# viridis_colors, scale = px.colors.convert_colors_to_same_type(px.colors.sequential.Pinkyl)
# colorscale = px.colors.make_colorscale(viridis_colors, scale=scale)
# print('viridis_colors', viridis_colors)
# print('scale', scale)
# print('colorscale', colorscale)
# print('----------------------')
from components.visual.utils.marker import test_marker_markup

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
access_token = os.environ['MAP_TOKEN']

testMapbox = MapBox(access_token)
query = 'lake garden taiping'
# lala = testMapbox.geocode(query=query, exactly_one=True, )
# print(lala)
# print(lala.longitude)
# print(lala.latitude)
# print(lala.address)
# print(lala.raw)


# fig = go.Figure(go.Scattermapbox(
#     mode="markers+text+lines",
#     lon=[-75, -80, -50], lat=[45, 20, -20],
#     marker={'size': 20, 'symbol': ["bus", "harbor", "airport"]},
#     text=["Bus", "Harbor", "airport"], textposition="bottom right"))
#
# print(fig)

layout = html.Div(
    [
        dcc.Store('resolution', data={'height':screen_height, 'width':screen_width}),
        html.Div('Welcome to Glance', id='empty-scene', className='empty-scene'),
        html.Div(id = 'visual-collection', children=[], className='visual-collection' ),
        select_dataset_modal.modal,
        # test_marker_markup(),

    ]
    ,className='main-container'

)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
