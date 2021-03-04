# import dash
# import dash_core_components as dcc
# import dash_html_components as html
#
# def render_scattermap(fx, add_clicks):
#     return html.Div(
#                 style={'width': '50%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10, 'position':'relative'},
#                 children=html.Div([
#                     dcc.Graph(id={'type': 'visualization', 'index': add_clicks}, figure=fx),
#                     html.Button('Delete', id={'type': 'dlt-btn', 'index': add_clicks}, style={'position':'absolute', 'top':0}),
#                 ]),
#             )