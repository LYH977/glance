
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc

def name_section_markup(create_clicks):
    return html.Div([
        dbc.Badge(create_clicks, pill=True, color="primary", className="mr-1"),
        dcc.Input(
            id={'type': 'visual-title', 'index': create_clicks},
            type="text",
            value=f'Visualization {create_clicks}',
            maxLength=18,
            autoFocus=False,
            autoComplete='off',
            size='13',
            className='visual-title'
        ),
    ], className='flex')