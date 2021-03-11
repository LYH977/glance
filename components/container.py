import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
from dash.exceptions import PreventUpdate
import tkinter as tk

from components import visualization, select_dataset_modal
from components.carousel import create_carousel
from components.visualization import create_visualization
from utils import collection
from utils.constant import CAROUSEL, FRAME
from utils.method import  set_slider_calendar

root = tk.Tk()
screen_width = root.winfo_screenwidth()

def render_container(create_clicks, param, ftype, tformat):
    # print('belum 2')

    data = collection.temp.dropna()
    df_frame = data[FRAME].unique()

    maxValue = df_frame.shape[0] - 1
    if(ftype != CAROUSEL):
        return create_visualization(screen_width, create_clicks, ftype, param, maxValue, df_frame, tformat)
    else:
        # print(collection.temp)
        return create_carousel(screen_width, create_clicks, param, maxValue, df_frame)
