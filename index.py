import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file

from app import app
from components.home.landing import landing_page

from pages import homepage, dashboard
from components import upload_modal, toast
from layout.navbar import navbar

from utils.method import reset_var



app.layout = html.Div([
    navbar,
    landing_page,

    html.Div(id='page-content', children=[]),
    upload_modal.layout,
    toast.layout

],
    className= 'index-layout'

)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home':
        reset_var()
        return homepage.layout
    if pathname == '/pages/visualization'  or pathname == '/':
        return dashboard.layout
    else:
        return pathname


# @app.callback(Output('upload-modal', 'is_open'),
#               [Input('upload-button', 'n_clicks'), Input('cancel-upload', 'n_clicks')],
#               State('upload-modal', 'is_open'),
#               prevent_initial_call = True)
# def update_output(open, close, is_open):
#     return not is_open


if __name__ == '__main__':
    app.run_server(
        debug=True,
        dev_tools_hot_reload = False,
        # host='192.168.0.123'
    )
