import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px

popover_children = [
    dbc.PopoverHeader("Mark a location"),
    dbc.PopoverBody(
        "And here's some amazing content. Cool!"
    ),
]

def marker_markup(create_clicks):
    return html.Div(
        [
            html.Span(
                html.I(className="fa fa-map-marker fa-lg"),
                # id={'type': 'marker-btn', 'index': create_clicks},
                id=f"popover-div-wrapper-{create_clicks}",
                n_clicks=0
            ),
            dbc.Popover(
                popover_children,
                id="legacy",
                # target="{'type': 'marker-btn', 'index': "+str(create_clicks)+"}",
                target=f"popover-div-wrapper-{create_clicks}",
                trigger="legacy",
                placement='bottom-end',
            ),


        ],

    )