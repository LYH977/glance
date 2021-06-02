import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    dbc.Toast(
            "No Message",
            id="my-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            duration = 2500,
            icon="danger",
            style={"position": "fixed", "bottom": 10, "left": 10, "width": 350,  'zIndex': 50, 'background': 'white'},
        ),
    dcc.Store(id='dashboard-toast', data=None),
    dcc.Store(id='upload-toast', data=None),
    dcc.Store(id='create-new-column-toast', data=None),
    dcc.Store(id='edit-toast', data=None),

])