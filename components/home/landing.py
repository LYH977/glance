import dash_html_components as html

landing_page = html.Div(
    html.Div([
        html.Div(className='clip-background'),
        html.Img(
                src='/assets/images/earth glance.jpeg',
                className='landing-img',
        ),
        html.P('See the world at a glance',className='landing-caption')
    ],className='clip-container'),


    id='empty-scene',
    className='landing-scene'
)