
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils.constant import MAXIMUM, MINIMUM, PERCENT


def collapse_markup(create_clicks, count):
    return html.Div([
        html.Div(
            # dbc.Row(
                [
                    notif_badge_markup(MAXIMUM, count[MAXIMUM], create_clicks),
                    notif_badge_markup(MINIMUM, count[MINIMUM], create_clicks),
                    notif_badge_markup(PERCENT, count[PERCENT], create_clicks),

                ],
            #     no_gutters=True,
            #     align='start',
            #     style={'overflowX': 'scroll'}
            # ),
            style={'overflow': 'auto',  'whiteSpace': 'nowrap'}

        ),
        html.Div(
            id={'type': 'notif-body-wrapper', 'index': create_clicks},
            className='notif-body-wrapper',
            # style={
            #     # 'display': 'hidden',
            #     'height': '0'  },
            children=dcc.Markdown(
                id={'type': 'notif-body', 'index': create_clicks},
                className='notif-body',

        )
        ),

    ])


def notif_badge_markup(id, number, create_clicks):
    # return dbc.Col(
       return dbc.Button(
            [
                id,
                dbc.Badge(number, color='light', className="ml-1", pill=True, id={'type': f'{id}-badge', 'index': create_clicks})
            ],
            color="dark",
            id={'type': f'{id}-notif', 'index': create_clicks},
           className='notif-badge'
        )
    #     ,width='auto',
    #     className= 'notif-badge'
    # )

def notif_loading_markup():
    return dbc.Spinner(
            color="light",
            type="grow"
        )