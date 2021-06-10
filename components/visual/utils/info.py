import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils.constant import SEQUENTIAL_COLOR, SCATTER_MAP, DENSITY


def info_table_markup(create_clicks, name1, type1,hidden):
    # hasMapbox = [SCATTER_MAP, DENSITY]
    # hidden = not type1 in hasMapbox
    formatted_name1 = name1 if len(name1) <16 else name1[0:15] + '...'
    table_header = [
        html.Thead(html.Tr([
            html.Th("No"),
            html.Th("Dataset"),
            html.Th("Type"),
            html.Th("Colorscale",style={'display': 'none'if hidden else 'block'  }),
            html.Th("Action"),
        ]))
    ]
    rows = []
    rows.append(
        html.Tr([
            html.Td(1),
            html.Td(formatted_name1),
            html.Td(type1),
            html.Td(
                dbc.Select(
                    id={'type': 'color-scale-dropdown', 'index': create_clicks},
                    options=[{"label": c, "value": c} for c in SEQUENTIAL_COLOR],
                    value='Pinkyl' ,
                    bs_size='sm'
                ),style={'display': 'none' if hidden else 'block' }
            ),
            html.Td(
                html.Span(
                    html.I(className="fa fa-edit fa-lg icon-btn icon-black"),
                    id={'type': 'edit-visual-btn', 'index': create_clicks},
                    n_clicks=0
                ),
            ),
        ]))
    rows.append(
        html.Tr([
            html.Td(2),
            html.Td('None',  id={'type': 'td-name-2', 'index': create_clicks},),
            html.Td('None', id={'type': 'td-type-2', 'index': create_clicks},),
            html.Td(
                dbc.Select(
                    id={'type': 'color-scale-dropdown-2', 'index': create_clicks},
                    options=[{"label": c, "value": c} for c in SEQUENTIAL_COLOR],
                    value= 'Plotly3', # 2nd Plotly3
                    bs_size= 'sm'
                ),style={'display': 'none'if hidden else 'block'  }
            ),
            html.Td(
                html.Span(
                    html.I(className="fa fa-trash fa-lg icon-btn icon-red"),
                    id={'type': 'del-secondary-btn', 'index': create_clicks},
                    n_clicks=0
                ),
            ),
        ],
        id={'type': 'tr-info-2', 'index': create_clicks},
        style= {'display': 'none' }
        ))
    table_body = [html.Tbody(rows)]
    return dbc.Table(
        table_header + table_body,
        bordered= True,
        responsive= True,
        hover= True,
        size='sm'
    )
#


def info_markup(create_clicks, name1, type1 ):
    hasMapbox = [SCATTER_MAP, DENSITY]
    hidden = not type1 in hasMapbox
    return html.Div(
        [
            dbc.Badge(
                create_clicks,
                id=f"popover-badge-{create_clicks}",
                pill=True,
                color="primary",
                className="mr-1 visual-badge",
                n_clicks=0
            ),
            dbc.Popover(

                [
                    info_table_markup(create_clicks, name1, type1, hidden),
                    html.Span(
                        html.I(className="fa fa-plus-square fa-lg icon-btn icon-black"),
                        id={'type': 'secondary-visual-btn', 'index': create_clicks},
                        n_clicks=0,
                        hidden= hidden
                    )
                ],
                id={'type': 'legacy-popover', 'index': create_clicks},
                target=f"popover-badge-{create_clicks}",
                trigger="legacy",
                placement='bottom-start',
            ),
        ],

    )