import pandas as pd

def configure_fig(fig):
    fig.layout.sliders[0].visible = False
    fig.layout.updatemenus[0].visible = False
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200

    fig.layout.coloraxis.colorbar.len = 0.5
    fig.layout.coloraxis.colorbar.yanchor = 'bottom'
    fig.layout.coloraxis.colorbar.xpad = 10
    fig.layout.coloraxis.colorbar.x =0
    fig.layout.coloraxis.colorbar.thickness = 10

    #white theme legend
    fig.layout.coloraxis.colorbar.bgcolor = 'rgba(255,255,255,0.5)' #'rgba(0,0,0,0.5)'
    fig.layout.coloraxis.colorbar.title.font.color = 'rgba(0,0,0,1)' #'rgba(255,255,255,1)'
    fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(0,0,0,1)' #'rgba(255,255,255,1)'

    fig.layout.margin.t = 0
    fig.layout.margin.b = 0
    fig.layout.margin.r = 0
    fig.layout.margin.l = 0
    fig.layout.updatemenus[0].showactive = True
    fig.layout.title.y = 0.98
    fig.layout.title.x = 0.02
    fig['layout']['uirevision'] = 1
    # fig.layout.autosize = False


def convert_to_float(data, parameter, list):
    for i in list:
        data[parameter[i]] = pd.to_numeric(data[parameter[i]])