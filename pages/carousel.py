import dash

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from app import app
from dash.exceptions import PreventUpdate


layout = html.Div([
    dcc.Interval(id='carousel-interval', interval=2000),
    html.Div(
        [
            html.Div(
                id="fade1",
                style={'position': 'absolute', 'top': 0, 'transition': 'opacity 1s'},
            ),
            html.Div(
                id="fade2",
                style={'position': 'absolute', 'top': 0,'transition': 'opacity 1s' },
            )
        ],
        style={'position':'relative'}
    ),


])



@app.callback([ Output('fade1', 'children'),Output('fade2', 'children') ,Output('fade1', 'style'),Output('fade2', 'style')  ],
              [ Input('carousel-interval', 'n_intervals') ],
              )
def display_image(interval):
    if interval == None or interval % 2 == 1:
        # print(interval, 'inside 1')
        img = html.Img(src="http://placeimg.com/625/225/arch")
        # img = html.Img(src="https://firebasestorage.googleapis.com/v0/b/glance-4685b.appspot.com/o/images%2Ftest.jpg?alt=media")

        return img,  dash.no_update , {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}

    elif interval % 2 == 0:
        # print(interval, 'inside 2')
        img = html.Img(src="http://placeimg.com/625/225/animals")
        # img = "None"
        return dash.no_update,  img,{'position': 'absolute', 'top': 0,'opacity':0.0, 'transition':'opacity 1s'}, {'position': 'absolute', 'top': 0,'opacity':1.0, 'transition':'opacity 1s'}

    else:
        raise PreventUpdate

