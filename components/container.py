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
from utils.constant import FRAME_NAME, CAROUSEL
from utils.method import  set_slider_calendar

root = tk.Tk()
screen_width = root.winfo_screenwidth()

def render_container(create_clicks, param, ftype):
    data = collection.temp.dropna()
    df_date = data[param[FRAME_NAME[ftype]]].unique()
    maxValue = df_date.shape[0] - 1
    if(ftype != CAROUSEL):
        return create_visualization(screen_width, create_clicks, ftype, param, maxValue, df_date)
    else:
        # print(collection.temp)
        return create_carousel(screen_width, create_clicks, param, maxValue, df_date)
