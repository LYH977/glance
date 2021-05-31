import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from components.visual.utils.controls import controls_markup
from components.visual.utils.intervals import intervals_markup
from components.visual.utils.marker import marker_markup
from components.visual.utils.name_section import name_section_markup
from components.visual.utils.setting import setting_markup
from components.visual.utils.stores import stores_markup


def visual_box_markup(create_clicks, param, figure, tformat, first_frame, dbname, now, new_col,maxValue, ):

    return html.Div(
        className='visual-box',
        children=[
            stores_markup(create_clicks, param, figure, tformat, first_frame, dbname, now, new_col),
            intervals_markup(create_clicks, maxValue),
            dbc.Row(
                [
                    dbc.Col(name_section_markup(create_clicks, dbname, param['vtype']), width='auto'),
                    dbc.Col(
                        dbc.Row([
                            dbc.Col(setting_markup(create_clicks, param['vtype'])),
                            dbc.Col(marker_markup(create_clicks, param['vtype'])),

                        ],justify="center"), width='auto', ),

                ],
                justify="around",
                align='center',
                style={'zIndex':20, 'background':'#46648c'}
            ),
            dcc.Graph(
                className='visualization',
                id={'type': 'visualization', 'index': create_clicks},
                style={'opacity':1},
                figure=figure,
                config={
                    'modeBarButtonsToRemove': [
                        'pan2d', 'select2d', 'lasso2d', 'zoomInMapbox', 'zoomOutMapbox', 'resetViewMapbox',
                        'toggleHover',
                        'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines',
                        'hoverClosestCartesian', 'hoverCompareCartesian', 'zoomInGeo', 'zoomOutGeo',
                        'hoverClosestGeo', 'resetGeo'
                    ],
                    'displaylogo': False,
                    # 'responsive': False,
                    # 'displayModeBar': False
                }
            ),
            html.Div(
                id={'type': 'option-wrapper', 'index': create_clicks},
                className='option-wrapper',
                style={'height': '15%', },  # 40% including card body
                children=[
                    controls_markup(create_clicks, maxValue, first_frame),
                    html.Div(
                        id={'type': "loading-notif-output", 'index': create_clicks},
                        children=dbc.Spinner(
                            color="light",
                            type="grow"
                        ),
                    ),
                ]
            ),
        ])