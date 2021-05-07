import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px

label_style  ={
            "color": "black",
        }
active_label_style  ={
            "color": "blue",
            'fontWeight':'bold',
        }
popover_children = [
    dbc.PopoverHeader("Mark a location"),
    dbc.PopoverBody(
        "And here's some amazing content. Cool!"
    ),
]


name_content = dbc.Card(
    dbc.CardBody(
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Name", addon_type="prepend", ),
                dbc.Input(placeholder="USM Malaysia"),
            ],
            className="mb-3", size="sm",
        )
    ),
    className="mt-3",
)

coordinate_content = dbc.Card(
    dbc.CardBody(
        [
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Latitude", addon_type="prepend", ),
                    dbc.Input(placeholder="12.12"),
                ],
                className="mb-3", size="sm",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Longitude", addon_type="prepend", ),
                    dbc.Input(placeholder="21.21"),
                ],
                className="mb-3", size="sm",
            ),
            dbc.Button("Confirm", color="success"),

        ]
    ),
    className="mt-3",
)



test_popover_children = [

    dbc.PopoverHeader(
        [
            dbc.Tabs([
                dbc.Tab(name_content, label="Name", label_style=label_style, active_label_style=active_label_style),
                dbc.Tab(coordinate_content, label="Coordinates",  label_style=label_style, active_label_style=active_label_style),
            ]),
            dbc.Button("Reset", color="danger"),
        ]
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


def test_marker_markup():
    return html.Div(
        [
            html.Span(
                html.I(className="fa fa-map-marker fa-lg"),
                # id={'type': 'marker-btn', 'index': create_clicks},
                id=f"popover-div-wrapper-",
                n_clicks=0
            ),
            dbc.Popover(
                test_popover_children,
                id="legacy",
                # target="{'type': 'marker-btn', 'index': "+str(create_clicks)+"}",
                target=f"popover-div-wrapper-",
                trigger="legacy",
                placement='bottom-end',
            ),
        ],

    )