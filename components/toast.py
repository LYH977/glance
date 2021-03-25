import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

layout = dbc.Toast(
            "No Message",
            id="my-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            duration = 5000,
            icon="danger",
            style={"position": "fixed", "top": 10, "right": 10, "width": 350, 'z-index': 100, 'background': 'white'},
        )