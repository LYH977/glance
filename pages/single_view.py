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
    # dcc.Store(id='play-btn-record', data=0),
    # dcc.Store(id='add-btn-record', data=0),
    dcc.Interval(
        id='interval',
        interval=200,
        n_intervals=0,
        max_intervals=maxValue,
        disabled=True
    ),
    html.Button('add visual', id='add-btn'),
    html.Div(id='visual-container', children=[]),
    dcc.Slider(
        id='anim-slider',
        updatemode='drag',
        min=0,
        max=50,
        value=0,
        marks={str(i): str(des) for i, des in zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
    ),
    html.Div([
        html.Button('play', id='play-btn'),
        html.Label(df_date[0], id='slider-label')
    ]),
    html.Label('nothing', id='clicker')

])


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




# update visualization container by appending or removing item from array
@app.callback(
     Output('visual-container', 'children') ,
    [ Input('add-btn', 'n_clicks'), Input({'type':'dlt-btn', 'index': ALL},'n_clicks') ],
    [ State('visual-container', 'children') ],
    prevent_initial_call=True)
def update_visual_container(add_clicks, deletable, div_children):
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(ctx.triggered)

    if input_id == 'add-btn': # input from add button
        new_child = html.Div(
            style={'width': '50%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
            children=html.Div([
                dcc.Graph(id={'type': 'visualization', 'index': add_clicks}, figure=visualization.fig),
                html.Button('Delete', id={'type': 'dlt-btn', 'index': add_clicks}, style={'position':'absolute', 'top':0}),
            ]),
        )
        print(div_children)
        div_children.append(new_child)
        return div_children
    else: # input from delete button
        delete_index = input_id.split(',')[0].split(':')[1]
        del div_children[int(delete_index) -1]
        return div_children



# update  figure according to slider
@app.callback(
    [Output({'type':'visualization', 'index': MATCH}, 'figure') ],
    [Input('anim-slider', 'value')],
    [State({'type':'visualization', 'index': MATCH}, 'figure')],
    prevent_initial_call = True)
def update_figure(value, fig):
    fig2 = fig
    # the code below is not necessary
    # fig2['layout']['sliders'][0]['active'] = value
    fig2['data'][0] = fig2['frames'][value]['data'][0]
    # data[1] is second figure
    # fig2['data'][1] =  {
    #      # "coloraxis":"coloraxis",
    #      "hovertemplate":data2['Date'].iloc[value]+"<br>Magnitude=%{z}<br>Lat=%{lat}<br>Long=%{lon}<extra></extra>",
    #      "lat":[
    #         data2['Lat'].iloc[value]
    #      ],
    #      "lon":[
    #         data2['Long'].iloc[value]
    #      ],
    #      "name":"",
    #      "radius":10,
    #      "subplot":"mapbox",
    #      "z":[
    #         data2['Magnitude'].iloc[value]
    #      ],
    #      "type":"densitymapbox",
    #      "showscale": False
    #   }
    return [fig2]



# update slider according to interval
@app.callback(
    Output('anim-slider', 'value'),
    [Input('interval', 'n_intervals')],
    State('is-animating', 'data')
)
def update_slider(value,animate):
    return value if animate is True else dash.no_update


# update play button label according to playing status
@app.callback(
    [Output('play-btn', 'children'), Output('interval', 'disabled')],
    [Input('is-animating', 'data')],
    prevent_initial_call=True
)
def update_play_btn(playing):
    if playing is True:
        return 'pause', False
    else:
        return 'play', True


# update playing status according to button click
@app.callback(
    [Output('is-animating', 'data'), Output('interval', 'n_intervals'), Output('slider-label', 'children')],
    [Input('play-btn', 'n_clicks'), Input('anim-slider', 'value')],
    [State('is-animating', 'data'), State('interval', 'n_intervals')],
    prevent_initial_call=True
)
def update_playing_status(play_clicked, s_value, playing, interval):
    ctx = dash.callback_context
    if not ctx.triggered:
        input_id = 'No input yet'
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id== 'anim-slider': #input from slider
        return \
            False if playing is True and s_value != interval or s_value == maxValue else dash.no_update,\
            dash.no_update, \
            df_date[s_value]

    elif  input_id== 'play-btn':#input from play btn
        return \
            not playing, \
            s_value if s_value != maxValue else 0, \
            dash.no_update

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