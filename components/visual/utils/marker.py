import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.constant import SCATTER_MAP, DENSITY

label_style  ={
            "color": "black",
        }
active_label_style  ={
            "color": "blue",
            'fontWeight':'bold',
        }


def namelist_item_not_found_markup(query):
    return dbc.ListGroupItem(
        [
            dbc.ListGroupItemHeading('Not Found', className='marker-item-heading'),
            dbc.ListGroupItemText(f"The query '{query}' was not found on this server", className='marker-item-text'),
        ], className='marker-group-item'
    )



def namelist_item_markup(name, coordinate, id, index, color=''):
    return dbc.ListGroupItem(
        [
            dbc.ListGroupItemHeading(
                name,
                className='marker-item-heading',
                id={'type': f'marker-name-{id}', 'index': index}
            ),
            dbc.ListGroupItemText(
                coordinate,
                className='marker-item-text' ,
                id={'type': f'marker-coordinate-{id}', 'index': index}
            ),
            dbc.Button(
                "apply",
                color="link",
                className='marker-item-btn',
                id={'type': f'marker-name-btn-{id}', 'index': index}
            )
        ], className='marker-group-item', color=color
    )



def name_markup(create_clicks):
    return dbc.Card(
        dbc.CardBody([
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Name", addon_type="prepend", ),
                    dbc.Input(
                        placeholder="e.g. USM Malaysia",
                        id={'type': 'marker-search-name', 'index': create_clicks},
                    ),
                ],
                className="mb-3", size="sm",
            ),
            dbc.ListGroup([
                # html.Div(style={'display':'block'},id={'type': 'marker-marked-name', 'index': create_clicks},),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading(
                            'name',
                            className='marker-item-heading',
                            id={'type': 'marked-name', 'index': create_clicks},

                        ),
                        dbc.ListGroupItemText(
                            'coordinate',
                            className='marker-item-text',
                            id={'type': 'marked-coordinate', 'index': create_clicks},

                        ),
                        dbc.Badge("Applied", color="success", className="mr-1 marker-item-btn"),
                    ],
                    style={'display':'none'},
                    id={'type': 'marker-marked-name', 'index': create_clicks},
                    color="success",
                    className='marker-group-item'
                ),
                html.Div(
                    id={'type': 'marker-namelist', 'index': create_clicks},
                    children=[

                    ]
                ),

            ],
                className='marker-namelist',
                # id={'type': 'marker-namelist', 'index': create_clicks}
            ),
            # dbc.Button("Confirm", color="success", id={'type': 'name-confirm-btn', 'index': create_clicks},),
        ]),
        className="mt-3",
    )

def coordinate_markup(create_clicks):
    return dbc.Card(
        dbc.CardBody([
            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Latitude", addon_type="prepend", ),
                    dbc.Input(
                        placeholder="( -85 to 85 )",
                        id={'type': 'latitude', 'index': create_clicks},
                        value=''
                    ),
                ],
                className="mb-3", size="sm",
            ),

            dbc.InputGroup(
                [
                    dbc.InputGroupAddon("Longitude", addon_type="prepend", ),
                    dbc.Input(
                        placeholder="( -180 to 180 )",
                        id={'type': 'longitude', 'index': create_clicks},
                        value= ''
                    ),
                    # dbc.FormText("Type something in the box above"),
                ],
                className="mb-3", size="sm",
            ),
            dbc.Button("Apply", color="success", disabled=True, id={'type': 'coordinate-apply-btn', 'index': create_clicks},),
        ]),
        className="mt-3",
    )


def popover_children_markup(create_clicks):
    return [
        dbc.PopoverHeader(
            [
                dbc.Tabs([
                    dbc.Tab(name_markup(create_clicks), label="Name", label_style=label_style, active_label_style=active_label_style),
                    dbc.Tab(coordinate_markup(create_clicks), label="Coordinates",  label_style=label_style, active_label_style=active_label_style),
                ]),
                dbc.Button("Reset", color="danger", id={'type': 'reset-marker-btn', 'index': create_clicks},),
            ],
            style={'maxWidth': '400px'},
        ),
    ]

def marker_markup(create_clicks, type):
    hasMapbox = [SCATTER_MAP, DENSITY]
    hidden = not type in hasMapbox
    return html.Div(
        [
            html.Span(
                html.I(className="fa fa-map-marker fa-lg"),
                id=f"popover-div-wrapper-{create_clicks}",
                n_clicks=0
            ),
            dbc.Popover(

                popover_children_markup(create_clicks),
                id="legacy",
                target=f"popover-div-wrapper-{create_clicks}",
                trigger="legacy",
                placement='bottom-end',
            ),
        ],
        hidden= hidden

    )


# def test_marker_markup():
#     create_clicks=1
#     return html.Div(
#         [
#             html.Span(
#                 html.I(className="fa fa-map-marker fa-lg"),
#                 # id={'type': 'marker-btn', 'index': create_clicks},
#                 id=f"popover-div-wrapper-",
#                 n_clicks=0
#             ),
#             dbc.Popover(
#                 popover_children_markup(create_clicks),
#                 id="legacy",
#                 # target="{'type': 'marker-btn', 'index': "+str(create_clicks)+"}",
#                 target=f"popover-div-wrapper-",
#                 trigger="legacy",
#                 placement='bottom-end',
#                 style={'maxWidth': '400px'},
#             ),
#         ],
#
#     )