import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

from pages import homepage, dashboard, upload_page
from components import carousel
from layout.navbar import navbar
from utils import collection
from utils.method import reset_var

app.layout = html.Div([
    navbar,
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home' or pathname == '/':
        reset_var()
        return homepage.layout
    if pathname == '/pages/singleView':
        return dashboard.layout
    if pathname == '/pages/upload':
        reset_var()
        return upload_page.layout
    else:
        return pathname


if __name__ == '__main__':
    app.run_server(debug=True)
