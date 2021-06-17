
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

from components.visual.utils.info import info_markup


def name_section_markup(create_clicks, name1, type1):
    return html.Div([
        info_markup(create_clicks, name1, type1),
        dcc.Input(
            id={'type': 'visual-title', 'index': create_clicks},
            type="text",
            value=f'{type1} {create_clicks}',
            maxLength=18,
            autoFocus=False,
            autoComplete='off',
            size='13',
            className='visual-title'
        ),
    ], className='flex')