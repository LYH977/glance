import pandas as pd
import plotly.graph_objects as go

from utils.constant import BAR_CHART_RACE

def configure_coloraxis(fig):
    fig.layout.coloraxis.colorbar.len = 0.99 #0.99
    fig.layout.coloraxis.colorbar.xpad = 5
    fig.layout.coloraxis.colorbar.ypad = 20
    fig.layout.coloraxis.colorbar.borderwidth = 0.1
    
    fig.layout.coloraxis.colorbar.x = -0.067
    fig.layout.coloraxis.colorbar.y = 0.01
    fig.layout.coloraxis.colorbar.title.side = 'right'
    fig.layout.coloraxis.colorbar.tickangle = -90
    fig.layout.coloraxis.colorbar.minexponent = 0
    fig.layout.coloraxis.colorbar.ticks = 'inside'
    fig.layout.coloraxis.colorbar.yanchor = 'bottom'
    fig.layout.coloraxis.colorbar.thickness = 7
    fig.layout.paper_bgcolor = '#fff'
    #white theme legend
    fig.layout.coloraxis.colorbar.bgcolor = 'rgba(255,255,255,1)' #'rgba(0,0,0,0.5)'
    fig.layout.coloraxis.colorbar.title.font.color = 'rgba(0,0,0,1)' #'rgba(255,255,255,1)'
    fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(0,0,0,1)' #'rgba(255,255,255,1)'



def configure_fig(fig, type, add_trace = False):
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
    fig.layout.updatemenus[0].showactive = True
    configure_coloraxis(fig)
    if type != BAR_CHART_RACE: #other than bar chart race
        fig.layout.margin.t = 0
        fig.layout.margin.b = 0
        fig.layout.margin.r = 0
        fig.layout.margin.l = 0
    else:                       # when bar chart race is chosen
        fig.layout.margin.t = 50
    fig.layout.title.y = 0.98
    fig.layout.title.x = 0.9
    fig.layout.title.text = fig['frames'][0]['name']
    fig.layout.title.font.color = 'red'
    fig.layout.title.font.size = 40
    fig['layout']['uirevision'] = 1
    if add_trace:
        temp = go.Figure(go.Scattermapbox(
            below='',
            showlegend=False,
            lat=[],
            lon=[],
            mode='markers',
            marker={'size': 0},
        ))
        fig.add_trace(temp['data'][0])
        fig.add_trace(temp['data'][0])



def convert_to_float(data, parameter, list):
    for i in list:
        data[parameter[i]] = pd.to_numeric(data[parameter[i]])