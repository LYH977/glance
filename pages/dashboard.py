import dash_html_components as html
from components import select_dataset_modal
import plotly.express as px

# from callback import upload_modal_callback
# from database import dbConfig
# px.colors.sequential.

# print('pltlys scale', px.colors.sequential.a )
print('sequential ', px.colors.PLOTLY_SCALES.keys() )
viridis_colors, scale = px.colors.convert_colors_to_same_type(px.colors.PLOTLY_SCALES["Viridis"])
colorscale = px.colors.make_colorscale(viridis_colors, scale=scale)
print('viridis_colors', viridis_colors)
print('scale', scale)
print('colorscale', colorscale)
print('----------------------')

layout = html.Div([
    html.Div('Welcome to Glance', id='empty-scene', className='empty-scene'),
    html.Div(id = 'visual-collection', children=[], className='visual-collection' ),
    select_dataset_modal.modal
, ], style={
    'position':'relative',
    # 'background':'#242444'
    }
)


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
