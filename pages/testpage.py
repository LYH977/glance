import datetime
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from app import app
from dash.dependencies import Input, Output, State, ClientsideFunction, MATCH
from dash.exceptions import PreventUpdate
import task
import os
import pandas as pd
import redis
import numpy as np
from datetime import datetime
from utils.export.export_data import export_mp4
from plotly import graph_objects as go
from copy import deepcopy
# import openpyxl as xl
#
# wb = xl.load_workbook('datasets/daily corona china.xlsx')
# sheet = wb['Sheet1']
#
# for row in range(3, sheet.max_row +1):
#     current_province = sheet.cell(row,3).value
#     current_confirm = sheet.cell(row,6).value
#     current_recovered = sheet.cell(row, 7).value
#     current_death = sheet.cell(row, 8).value
#
#     # current_new_confirm = sheet.cell(row, 9).value
#     # current_new_recover = sheet.cell(row, 10).value
#     # current_new_death = sheet.cell(row, 11).value
#
#     previous_province = sheet.cell(row-1, 3).value
#     previous_confirm = sheet.cell(row-1, 6).value
#     previous_recovered = sheet.cell(row-1, 7).value
#     previous_death = sheet.cell(row-1, 8).value
#
#     if current_province == previous_province:
#         sheet.cell(row, 10).value = current_confirm - previous_confirm
#         sheet.cell(row, 11).value = current_recovered - previous_recovered
#         sheet.cell(row, 12).value = current_death - previous_death
#     else:
#         sheet.cell(row, 10).value = current_confirm
#         sheet.cell(row, 11).value = current_recovered
#         sheet.cell(row, 12).value = current_death
# wb.save('settle.xlsx')

redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
N = 100
df = pd.DataFrame(
    {
        "time": [
            i
            for i in range(N)
        ],
        "value": np.random.randn(N),
    }
)

################################################################################################################
# data = pd.read_csv('C:/Users/FORGE-15/PycharmProjects/glance/datasets/time-series-19-covid-combined.csv')
# fig = px.scatter_mapbox(
#         data, lat = 'Lat',
#         lon = 'Long',
#         size = 'Confirmed', size_max = 50,
#         color = 'Deaths', color_continuous_scale = px.colors.sequential.Pinkyl,
#         hover_name = 'Country/Region',
#         mapbox_style = 'light', zoom=1,
#         title='testing',
#         animation_frame='Date',
#     )
# fig.layout.margin.t = 0
# fig.layout.margin.b = 0
# fig.layout.margin.r = 0
# fig.layout.margin.l = 0
#
# fig.layout.title.pad.t = 0
# fig.layout.title.pad.b = 0
# fig.layout.title.pad.r = 0
# fig.layout.title.pad.l = 0
# fig.layout.title.font.color = 'red'
# fig.layout.title.font.size = 50
# fig.layout.title.y = 0.98
# fig.layout.title.x = 0.2
#
# fig.layout.coloraxis.colorbar.len = 0.49
# fig.layout.coloraxis.colorbar.yanchor = 'bottom'
# # fig.layout.coloraxis.colorbar.xanchor = 'right'
#
# fig.layout.coloraxis.colorbar.xpad = 7
# # fig.layout.coloraxis.colorbar.ypad = 50
#
# fig.layout.coloraxis.colorbar.x = -0.04
# fig.layout.coloraxis.colorbar.y = 0.5
# fig.layout.coloraxis.colorbar.thickness = 10
#
# # fig.layout.coloraxis.colorbar.outlinewidth =1
#
# fig.layout.coloraxis.colorbar.borderwidth = 0.1
#
# # #dark
# # fig.layout.coloraxis.colorbar.bgcolor = 'rgba(0,0,0,1)'
# # fig.layout.coloraxis.colorbar.title.font.color = 'rgba(255,255,255,1)'
# # fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(255,255,255,1)'
# #white
# fig.layout.coloraxis.colorbar.bgcolor = 'rgba(255,255,255,1)'
# fig.layout.coloraxis.colorbar.title.font.color = 'rgba(0,0,0,1)'
# fig.layout.coloraxis.colorbar.tickfont.color = 'rgba(0,0,0,1)'
# #
# fig.layout.sliders[0].visible = False
# fig.layout.updatemenus[0].visible = False


######################################################################################################

# access_token = os.environ['MAP_TOKEN']
#
# fig = go.Figure(go.Scattermapbox(
#     mode = "markers+text+lines",
#     lon = [-75, -80, -50], lat = [45, 20, -20],
#     marker = {'size': 20, 'symbol': ["marker", "harbor", "airport"]},
#     text = ["Bus", "Harbor", "airport"],
#     textposition = "top center"
# ))
#
#
# fig.update_layout(
#     mapbox = {
#         'accesstoken': access_token,
#         'style': "outdoors", 'zoom': 0.7},
#     showlegend = True
# )
################################################################################################################
table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")], style={'display': 'none'})
row4 = html.Tr([html.Td("Trillian"), dbc.Select(
    options=[
        {"label": "Option 1", "value": "1"},
        {"label": "Option 2", "value": "2"},
        {"label": "Disabled option", "value": "3", "disabled": True},
    ],
)])

table_body = [html.Tbody([row1, row2, row3, row4])]

table = dbc.Table(
    table_header + table_body,
    borderless=True,
    responsive= True,
     hover= True,
    size='sm'
)


################################################################################################################
toast = html.Div(
    [
        dbc.Button(
            "Open toast", id="positioned-toast-toggle", color="primary"
        ),
        dbc.Toast(
            "This toast is placed in the top right",
            id="positioned-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            duration=5000,

            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 0, "right": 10, "width": 350, 'background': 'white'},
        ),

    ]
)
################################################################################################################
layout = dbc.Jumbotron(
    [   toast,
        # html.Span(id='submit-button', n_clicks=0, className='fa fa-send'),
        dcc.Download(id="new-download"),
        html.Button('test new dl btn', id='new-dl-btn'),
        # dcc.Store(id='testing-js', data=fig),
        # dcc.Store(id='testing-plot', data= fig),
        html.Button('multiple layer figure', id='multi-layer-btn'),
        html.Span(
            html.I(className="fa fa-cog fa-lg icon-btn"),
            id=f"popover-setting-wrapper-",
            n_clicks=0,
            style={'color':'grey'},
            className='icon-btn-wrapper'
        ),

        # dcc.Graph(id='hp-fig', figure = fig, config={
        #             'modeBarButtonsToRemove': [
        #                 'pan2d', 'select2d', 'lasso2d', 'zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox',
        #                 'toggleHover',
        #                 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines',
        #                 'hoverClosestCartesian', 'hoverCompareCartesian', 'zoomInGeo', 'zoomOutGeo',
        #                 'hoverClosestGeo', 'resetGeo'
        #             ],
        #             'displaylogo': False,
        #             # 'responsive': False,
        #             # 'displayModeBar': False
        #         }),
        html.A('Download test.mp4', id='export-test-link',
               download='',
               href='',
               hidden= True),
        html.Button('export btn', id='export-test-btn'),
        dcc.Store(id='export-test-name', data= None),

        dcc.Interval(
                id= 'export-test-interval',
                interval=1000,
                n_intervals=0,
                disabled=True
            ),

        html.Button('client', id={'type': 'client-btn', 'index': 1}),
        html.Button('simulator', id={'type': 'sim-btn', 'index': 1}),

        html.P(
            "initial\n1",
            className="lead",
            id={'type': 'client-p', 'index': 1},
            style={"whiteSpace": "pre"}
        ),
        html.Button('test2', id='test2'),
        html.P(
            "avenger assem,ble",
            className="lead",
            id='title2'
        ),
        html.Button('testcelery', id='testcelery'),
        html.H1("Glance", className="display-3"),
        html.P(
            "Watch the world with a glance",
            className="lead",
            id='title'
        ),
        html.Hr(className="my-2"),
        html.P(
            "Jumbotrons use utility classes for typography and "
            "spacing to suit the larger container."
        ),
        html.P(dbc.Button("Learn more", color="primary"), className="lead"),
        table


    ]
)

# ############################################################################################################################################



@app.callback(Output('title', 'children'),
              Input('testcelery', 'n_clicks'))
def update_output(click):
    if click is not None:
        # lala = redis_instance.hset( "new" )
        lala = redis_instance.get('new').decode("utf-8")
        # print('see here:',lala)

        return 'dd'
# ############################################################################################################################################


@app.callback(Output('title2', 'children'),
              Input('test2', 'n_clicks'))
def update_output(click):
    if click is not None:
        # print('clicked test2')
        task.update_data.delay(2)
        return 'spider'


# ############################################################################################################################################




app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='second_function'
    ),
    Output({'type': 'client-p', 'index': MATCH}, 'children'),
    Input({'type': 'client-btn', 'index': MATCH}, 'n_clicks'),
    Input({'type': 'sim-btn', 'index': MATCH}, 'n_clicks'),
    prevent_initial_call=True
)

# ############################################################################################################################################


@app.callback(
    Output("positioned-toast", "is_open") ,
    [Input("positioned-toast-toggle", "n_clicks")],
    State("hp-fig", "figure"),
    prevent_initial_call=True
)
def open_toast(n,figure):
    print(figure)
    if n:
        return True
    return False

# ############################################################################################################################################

@app.callback(
    [
        Output("export-test-link", "download"),
        Output("export-test-link", "href"),
        Output("export-test-link", "hidden"),
        Output("export-test-btn", "hidden"),
    ] ,
    [Input("export-test-btn", "disabled")],
    [State('export-test-name', 'data'), State('hp-fig', 'figure')],
    prevent_initial_call=True

)
def open_toast(disabled, name, fig):
    if disabled:
        export_mp4(fig, name)
        dl = f'{name}.mp4'
        # path = f'/assets/export/{dl}'
        path =  app.get_asset_url(f'export/{dl}')
        print(f'habis href {name}')
        return dl, path, False, True
    else:
        return None, None, True, dash.no_update

# ############################################################################################################################################

@app.callback(
    [
        Output("export-test-btn", "disabled"),
        Output("export-test-interval", "disabled"),
        Output("export-test-name", "data"),
    ] ,
    [Input("export-test-btn", "n_clicks")],
    State("export-test-btn", "disabled"),
    prevent_initial_call=True
)
def open_toast(btn_click, disabled):

    if  btn_click and not disabled :
        now = int(datetime.now().timestamp())
        return True, False, now

    raise PreventUpdate

# ############################################################################################################################################

@app.callback(
    Output("export-test-interval", "n_intervals"),
    [Input("export-test-link", "n_clicks")],
    prevent_initial_call=True
)
def open_toast( click):
    return 0

# ############################################################################################################################################

@app.callback(
    Output("new-download", "data"),
    [Input("new-dl-btn", "n_clicks")],
    prevent_initial_call=True
)
def open_toast( click):
    return dcc.send_file('./assets/export/1618304344.mp4')

# ############################################################################################################################################

@app.callback(
    Output("hp-fig", "figure"),
    [Input("multi-layer-btn", "n_clicks")],
    State("hp-fig", "figure"),

    prevent_initial_call=True
)
def open_toast( click, fig):
    if click:

        temp = deepcopy(fig['data'][0])
        fig['data'].append(temp)
        fig['data'][1]['marker']['coloraxis'] = 'coloraxis2'
        fig['data'][1]['lat']= [-27.059125784374054]
        fig['data'][1]['lon']= [82.968750]
        fig['data'][1]['hovertext']= ['eren jaegar']
        fig['data'][1]['marker']['color']= [17]
        fig['data'][1]['marker']['size']= [444]

        temp_coloraxis = deepcopy(fig['layout']['coloraxis'])
        fig['layout']['coloraxis2'] = temp_coloraxis
        fig['layout']['coloraxis2']['colorbar']['bgcolor'] = "rgba(120,20,200,1)"
        fig['layout']['coloraxis2']['colorbar']['title']['text'] = 'testing'
        fig['layout']['coloraxis2']['colorbar']['y'] = 0
        # print(fig)
        return fig
    raise PreventUpdate