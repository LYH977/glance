import dash_html_components as html

from components import select_dataset_modal

# from callback import upload_modal_callback
# from database import dbConfig


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
