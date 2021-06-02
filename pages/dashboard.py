import dash_html_components as html
import os
import plotly.graph_objects as go

from components import select_dataset_modal
import plotly.express as px
import dash_core_components as dcc
import tkinter as tk
from geopy.geocoders import MapBox

from components.edit_visual_modal import edit_modal
from components.home.landing import landing_page

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


layout = html.Div(
    [

        dcc.Store('resolution', data={'height':screen_height, 'width':screen_width}),
        html.Div(id = 'visual-collection', children=[], className='visual-collection' ),
        select_dataset_modal.modal,
        edit_modal

    ]
    ,className='main-container'

)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
