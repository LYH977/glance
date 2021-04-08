import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import base64



navbar = dbc.NavbarSimple(
    children=[
        dcc.Location(id='url', refresh=False),
        # dbc.NavItem(dbc.NavLink("Home", href="/pages/home"),active=True),
        # dbc.NavItem(dbc.NavLink("Visualization", href="/pages/visualization"), active=True),
        # dbc.NavItem(dbc.NavLink("old", href="/pages/upload"), active=True),
        dbc.NavItem(
            dbc.NavLink(
                html.I(className="fa fa-upload"),
                id='upload-button',
                n_clicks=0
            ),
            active=True ,
            className='nav-item'
        ),

    ],
    brand="Glance",
    brand_href="/pages/home",
    color="dark",
    dark=True,
)


