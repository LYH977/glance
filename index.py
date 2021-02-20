import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

from pages import homepage, dashboard, carousel
from layout.navbar import navbar


app.layout = html.Div([
    navbar,
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home' or pathname == '/':
        return homepage.layout
    if pathname == '/pages/singleView':
        return dashboard.layout
    if pathname == '/pages/carousel':
        return carousel.layout
    else:
        return pathname


if __name__ == '__main__':
    app.run_server(debug=True)
