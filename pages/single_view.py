import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

from app import app

# from database import dbConfig
from components import visualization
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
from dash.exceptions import PreventUpdate


def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
        value = dataframe[i] if i % 7 == 0 else ''
        calendar.append(value)
    return calendar


data = visualization.data
data2 = visualization.data2

df_date = data['Date'].unique()
maxValue = df_date.shape[0] - 1

layout = html.Div([
    dcc.Store(id='is-animating', data=False),
    dcc.Store(id='play-btn-record', data=0),
    dcc.Store(id='add-btn-record', data=0),
    dcc.Interval(
        id='slider-interval',
        interval=200,
        n_intervals=0,
        max_intervals=maxValue,
        disabled=True
    ),
    html.Button('add visual', id='add-btn'),
    html.Button('add test', id='add-test'),
    html.Div(id='visual-container', children=[]),
    dcc.Slider(
        id='anim-slider',
        updatemode='drag',
        min=0,
        max=500,
        value=0,
        # marks={str(i): str(des) for i, des in zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
        # marks={str(i): str(i) for i in range(0, 500)},

    ),
    # daq.Slider(
    #     id='anim-slider',
    #     min=0,
    #     max=40,
    #     value=0,
    #     size=500,
    #     handleLabel={"showCurrentValue": False,"label": '2020-01-22', 'style':{'width': '50%', 'height':'150%','font-size':'400px'}},
    #     marks={
    #             0: '2020-01-22',
    #             10: '2020-01-29',
    #             20: '2020-02-05',
    #             30: '2020-02-12',
    #             40: '2020-02-19'
    #         }
    # )  ,
    html.Div([
        html.Button('play', id='play-btn'),
        html.Label(df_date[0], id='slider-label')
    ]),
    html.Label('nothing', id='clicker')

])


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# update fig according to interval
@app.callback(
    Output({'type': 'deletable', 'index': MATCH}, 'data'),
    [Input({'type':'dlt-btn', 'index': MATCH},'n_clicks')],
    # [State({'type': 'deletable', 'index': MATCH}, 'data')],
)
def mark_deletable(value):
    return True


# append new visualization to the container array
@app.callback(
    [ Output('visual-container', 'children'), Output('add-btn-record', 'data') ],
    [ Input('add-btn', 'n_clicks'), Input({'type':'deletable', 'index': ALL},'data') ],
    [ State('visual-container', 'children'), State('add-btn-record', 'data') ],
    prevent_initial_call=True)
def display_graphs(add_clicks, deletable, div_children, prev_clicked):
    if add_clicks and add_clicks != prev_clicked:
        new_child = html.Div(
            style={'width': '50%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
            children=html.Div([
                dcc.Graph(id={'type': 'visualization', 'index': add_clicks}, figure=visualization.fig),
                html.Button('Delete', id={'type': 'dlt-btn', 'index': add_clicks}, style={'position':'absolute', 'top':0}),
                dcc.Store(id={'type': 'deletable', 'index': add_clicks}, data=False),
            ]),
        )
        print('delete',deletable)
        div_children.append(new_child)
        return div_children,add_clicks
    else:
        index = deletable.index(True)
        del div_children[index]
        return div_children, dash.no_update



# update figure
@app.callback(
    [Output({'type':'visualization', 'index': MATCH}, 'figure') ],
    [Input('anim-slider', 'value')],
    [State({'type':'visualization', 'index': MATCH}, 'figure')],
    prevent_initial_call = True)
def update_slider(value, fig):
    fig2 = fig
    fig2['layout']['sliders'][0]['active'] = value
    fig2['data'][0] = fig2['frames'][value]['data'][0]
    print(fig)
    fig2['data'][1] =  {
         # "coloraxis":"coloraxis",
         "hovertemplate":data2['Date'].iloc[value]+"<br>Magnitude=%{z}<br>Lat=%{lat}<br>Long=%{lon}<extra></extra>",
         "lat":[
            data2['Lat'].iloc[value]
         ],
         "lon":[
            data2['Long'].iloc[value]
         ],
         "name":"",
         "radius":10,
         "subplot":"mapbox",
         "z":[
            data2['Magnitude'].iloc[value]
         ],
         "type":"densitymapbox",
         "showscale": False
      }
    return [fig2]



# update fig according to interval
@app.callback(
    Output('anim-slider', 'value'),
    [Input('slider-interval', 'n_intervals')],
)
def update_slider(value):
    return value


# update play button according to playing status
@app.callback(
    [Output('play-btn', 'children'), Output('slider-interval', 'disabled')],
    [Input('is-animating', 'data')],
    prevent_initial_call=True
)
def testing(playing):
    if playing is True:
        return 'pause', False
    else:
        return 'play', True


# update playing status according to button click
@app.callback(
    [Output('is-animating', 'data'), Output('play-btn-record', 'data'), Output('slider-interval', 'n_intervals')],
    [Input('play-btn', 'n_clicks'), Input('anim-slider', 'value')],
    [State('is-animating', 'data'), State('slider-interval', 'n_intervals'), State('play-btn-record', 'data')],
    prevent_initial_call=True
)
def testing(play_clicked, s_value, playing, interval, prev_clicked):
    if play_clicked and play_clicked != prev_clicked:
        return not playing, play_clicked, s_value if s_value != maxValue else 0
    else:
        if playing is True and s_value != interval or s_value == maxValue:
            return False, dash.no_update, dash.no_update
        else:
            raise PreventUpdate




    # focus onto certain location and zoom in
    # if graph_click_data and graph_click_data != prev_graph_click_data:
    #     data_link = graph_click_data
    #     fig2['layout']['mapbox']['center']['lat'] = data_link['points'][0]['lat']
    #     fig2['layout']['mapbox']['center']['lon'] = data_link['points'][0]['lon']
    #     fig2['layout']['mapbox']['zoom'] = 5
    #     print('matched')

    # @app.callback(
    #     Output('test-container', 'children'),
    #     [Input('add-test', 'n_clicks')],
    #     [State('test-container', 'children')],
    #     prevent_initial_call=True)
    # def display_test(n_clicks, div_children):
    #     new_child = html.Label(
    #         'erenJaegar ', id={'type': 'test', 'index': n_clicks}
    #     )
    #     div_children.append(new_child)
    #     return div_children

    # @app.callback(
    #     [Output({'type':'test', 'index': MATCH}, 'children') ],
    #     [Input('anim-slider', 'value')],
    #     [State({'type':'test', 'index': MATCH}, 'id')],
    #     prevent_initial_call = True)
    # def update_slider(value, fig):
    #     return [fig['index']]