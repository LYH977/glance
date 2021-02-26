# import dash
#
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import pandas as pd
# from dash.dependencies import Input, Output, State
# from app import app
# from dash.exceptions import PreventUpdate
#
# df = pd.read_csv(r'C:\Users\FORGE-15\PycharmProjects\glance\datasets\urban.csv')
# image = []
# for row in df.index:
#     image.append(html.Img(src=df.loc[row,'link']))
#
# layout = html.Div([
#     dcc.Interval(id='carousel-interval', interval=1000, max_intervals=34, n_intervals= 0),
#     html.Label(id='ca-label'),
#     html.Div(
#         [
#             html.Div(
#                 id="fade1",
#                 style={'position': 'absolute', 'top': 0, 'transition': 'opacity 1s'},
#             ),
#             html.Div(
#                 id="fade2",
#                 style={'position': 'absolute', 'top': 0,'transition': 'opacity 1s' },
#             )
#         ],
#         style={'position':'relative'}
#     ),
#
#
# ])
#
#
#
# @app.callback([ Output('fade1', 'children'),Output('fade2', 'children')  ,Output('ca-label', 'children')
#                   # ,Output('fade1', 'style'),Output('fade2', 'style')
#                 ],
#               [ Input('carousel-interval', 'n_intervals') ],
#               )
# def display_image(interval):
#     if interval == None or interval % 2 == 1:
#         # print(interval, 'inside 1')
#         # img = html.Img(src="http://placeimg.com/625/225/arch")
#         img = image[interval]
#         # img = html.Img(src="https://firebasestorage.googleapis.com/v0/b/glance-4685b.appspot.com/o/images%2Ftest.jpg?alt=media")
#
#         return img,  dash.no_update , df.loc[interval,'year']
#             # , {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}
#
#     elif interval % 2 == 0:
#         # print(interval, 'inside 2')
#         # img = html.Img(src="http://placeimg.com/625/225/animals")
#         img = image[interval]
#
#         # img = "None"
#         return dash.no_update,  img , df.loc[interval,'year']
#             # ,{'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}
#
#     else:
#         raise PreventUpdate
#
