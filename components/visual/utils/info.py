import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils.constant import SEQUENTIAL_COLOR, SCATTER_MAP, DENSITY


def info_table_markup(create_clicks, name1, type1):
    hasMapbox = [SCATTER_MAP, DENSITY]
    hidden = not type1 in hasMapbox
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
            html.Td(name1),
            html.Td(type1),
            html.Td(
                dbc.Select(
                    id={'type': 'color-scale-dropdown', 'index': create_clicks},
                    options=[{"label": c, "value": c} for c in SEQUENTIAL_COLOR],
                    value='Pinkyl'  # 2nd Pinkyl
                ),style={'display': 'none' if hidden else 'block' }
            ),
            html.Td('action'),
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
                    value= 'Plotly3' # 2nd Plotly3
                ),style={'display': 'none'if hidden else 'block'  }
            ),
            html.Td('action',id={'type': 'td-action-2', 'index': create_clicks},),

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
    return html.Div(
        [
            dbc.Badge(
                create_clicks,
                id=f"popover-badge-{create_clicks}",
                pill=True,
                color="primary",
                className="mr-1",
                n_clicks=0
            ),
            dbc.Popover(

                info_table_markup(create_clicks, name1, type1,),
                id="legacy",
                target=f"popover-badge-{create_clicks}",
                trigger="legacy",
                placement='bottom-start',
            ),
        ],

    )