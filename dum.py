import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import numpy as np
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)


def set_slider_calendar(dataframe):
    calendar = []
    for i in range(0, dataframe.shape[0]):
        value = dataframe[i] if i % 7 == 0 else ''
        calendar.append(value)
    return calendar


access_token = 'pk.eyJ1IjoiZ2xhbmNlYXBwIiwiYSI6ImNrZ20xYnBkNTA0dnYydm10ZXB4cGVyNjIifQ.q23_rB25-GjegLJ48R3NBQ'
data_url = 'https://shahinrostami.com/datasets/time-series-19-covid-combined.csv'
data = pd.read_csv(data_url)
missing_states = pd.isnull(data['Province/State'])
data.loc[missing_states, 'Province/State'] = data.loc[missing_states, 'Country/Region']
data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
for i in range(0, data.shape[0]):
    data.loc[i, 'Size'] = data.loc[i, 'Active'] if data.loc[i, 'Active'] < 50 else 50
data = data.dropna()
df_date = data['Date'].unique()

testingtrace=[]
for j in range(0, df_date.shape[0]):
    trace=[]
    filtered_df = data[data['Date'] == df_date[j]]
    for i in filtered_df['Province/State'].unique():
        df_by_continent = filtered_df[filtered_df['Province/State'] == i]
        trace.append(
            go.Scattermapbox(
                lat=df_by_continent['Lat'],
                lon=df_by_continent['Long'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=df_by_continent['Size']
                ),
                text=df_by_continent['Province/State'],

            )
        )
    testingtrace.append(trace)

app.layout = html.Div([
    dcc.Interval(
        id='interval',
        interval=1000,
        n_intervals=0,
        max_intervals=df_date.shape[0] - 1,
        disabled=True
    ),
    dcc.Graph(id='my_graph'),
    dcc.Slider(
        id='slider',
        min=0,
        max=df_date.shape[0] - 1,
        value=0,
        marks={str(i): str(des) for i, des in zip(range(0, df_date.shape[0]), set_slider_calendar(df_date))},
        dots=True
    ),
    html.Div(id='label', style={'margin-top': 20}),
    html.Button('Play', id='my_btn'),
])


@app.callback([Output('interval', 'disabled'), Output('my_btn', 'children')],
              [Input('my_btn', 'n_clicks')],
              [State('interval', 'disabled')])
def display_value(click, value):
    print('click', value)
    if click:
        new_value = not value
        btn_name = 'Play' if new_value else 'Pause'
        return new_value, btn_name
    else:
        raise PreventUpdate


@app.callback(Output('label', 'children'),
              [Input('slider', 'value')])
def display_value(value):
    return f'Selected Calendar: {df_date[value]} '


@app.callback(Output('slider', 'value'),
              [Input('interval', 'n_intervals')])
def update_slider(num):
    return num


@app.callback(
    Output('my_graph', 'figure'),
    [Input('slider', 'value')])
def update_figure(selected_year):
    print('selected_year',selected_year)
    # filtered_df = data[data['Date'] == df_date[selected_year]]
    # traces = []
    # for i in filtered_df['Province/State'].unique():
    #     df_by_continent = filtered_df[filtered_df['Province/State'] == i]
    #     traces.append(
    #         go.Scattermapbox(
    #             lat=df_by_continent['Lat'],
    #             lon=df_by_continent['Long'],
    #             mode='markers',
    #             marker=go.scattermapbox.Marker(
    #                 size=df_by_continent['Size']
    #             ),
    #             text=df_by_continent['Province/State'],
    #
    #         )
    #     )

    return {
        'data': testingtrace[selected_year],
        'layout': dict(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                accesstoken=access_token,
                bearing=0,
                center=dict(
                    lat=38.92,
                    lon=-77.07
                ),
                pitch=0,
                zoom=1
            ),
            transition={
                'duration': 500,
                'easing': 'linear'
            }
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)

# import dash
# import dash_html_components as html
# import dash_core_components as dcc
# import numpy as np
#
# from dash.dependencies import Input, Output
#
# # Example data (a circle).
# resolution = 20
# t = np.linspace(0, np.pi * 2, resolution)
# x, y = np.cos(t), np.sin(t)
# # Example app.
# figure = dict(data=[{'x': [], 'y': []}], layout=dict(xaxis=dict(range=[-1, 1]), yaxis=dict(range=[-1, 1])))
# app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
# app.layout = html.Div([dcc.Graph(id='graph', figure=figure), dcc.Interval(id="interval")])
#
#
# @app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
# def update_data(n_intervals):
#     index = n_intervals % resolution
#     print('index',index)
#     # tuple is (dict of new data, target trace index, number of points to keep)
#     return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
#
#
# if __name__ == '__main__':
#     app.run_server()