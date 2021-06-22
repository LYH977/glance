
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def visual_mask_markup(create_clicks):
    return html.Div(
        id = {'type': 'visual-mask', 'index': create_clicks},
        className ='visual-mask',
        style={'zIndex':19},
        children= [
            html.I(className="fa fa-arrow-left", id={'type': 'left-arrow', 'index': create_clicks}, style={'color':'#dbdbdb'} ),
            html.Div(create_clicks, className= 'id-circle'),
            html.I(className="fa fa-arrow-right", id={'type': 'right-arrow', 'index': create_clicks}, style={'color':'#dbdbdb'} ),
        ]
    )