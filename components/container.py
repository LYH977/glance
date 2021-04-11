import tkinter as tk

from components.carousel import create_carousel
from components.visual.visualization import create_visualization
from utils import collection
from utils.constant import CAROUSEL, FRAME

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

def render_container(create_clicks, param, tformat, dbname, now, new_col):
    data = collection.temp.dropna()
    df_frame = data[FRAME].unique()
    maxValue = df_frame.shape[0] - 1
    if(param['vtype'] != CAROUSEL):
        return create_visualization(screen_height, screen_width, create_clicks,  param, maxValue, df_frame, tformat, dbname, now, new_col)
    else:
        # print(collection.temp)
        return create_carousel(screen_height, screen_width, create_clicks,  param['parameter'], maxValue, df_frame, tformat, dbname)
