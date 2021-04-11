import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

def setting_markup(create_clicks):
    return dbc.DropdownMenu(
                        label = 'setting',
                        children = [

                            dbc.DropdownMenuItem(
                                daq.BooleanSwitch(
                                    id = {'type': 'legend-theme', 'index': create_clicks},
                                    on = False,
                                    color = "#000000",
                                    label = 'Legend Theme'
                                ),
                                header = True
                            ),

                            dbc.DropdownMenuItem(
                                daq.BooleanSwitch(
                                    id = {'type': 'live-mode', 'index': create_clicks},
                                    on = False,
                                    color = "#9B51E0",
                                    label = f'Live Mode {create_clicks}'

                                ),
                                header = True
                            ),

                            dbc.DropdownMenuItem(
                                dbc.Button(
                                    'Delete',
                                    id = {'type': 'dlt-btn', 'index': create_clicks},
                                    color = "danger",
                                    className = "mr-1"
                                ) ,
                                header = True
                            ),

                            dbc.DropdownMenuItem(
                                html.Div([
                                    dbc.Button(
                                        'Generate MP4',
                                        id = {'type': 'export-btn', 'index': create_clicks},
                                        color = "info",
                                        className = "mr-1"
                                    ),
                                    html.A(
                                        'Download MP4',
                                        id = {'type': 'export-link', 'index': create_clicks},
                                        download = '',
                                        href = '', #/assets/test.mp4
                                        hidden = True
                                    ),
                                ]),

                                header = True
                            ),
                        ],
                    )