import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

def controls_markup(create_clicks, maxValue, initial_label):
    return dbc.Row([
                dbc.Col(
                    dbc.Button(
                        'Play',
                        id={'type': 'play-btn', 'index': create_clicks},
                        color="light",
                        size='sm',
                        className='play-btn'
                    ), width='auto'
                ),
                # dbc.Col(html.Label(initial_label, id={'type': 'slider-label', 'index': create_clicks},
                #                    style={'color': 'white'}), width='auto'),
                dbc.Col(dcc.Slider(
                    id={'type': 'anim-slider', 'index': create_clicks},
                    updatemode='drag',
                    min=0,
                    max=maxValue,
                    value=0,
                )),
            ], className= 'control-style')