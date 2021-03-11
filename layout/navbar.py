import dash_bootstrap_components as dbc
import dash_core_components as dcc

navbar = dbc.NavbarSimple(
    children=[
        dcc.Location(id='url', refresh=False),
        dbc.NavItem(dbc.NavLink("Home", href="/pages/home"),active=True),
        dbc.NavItem(dbc.NavLink("Visualization", href="/pages/visualization"), active=True),
        # dbc.NavItem(dbc.NavLink("old", href="/pages/upload"), active=True),
        dbc.NavItem(dbc.NavLink("Upload",id='upload-button', n_clicks=0), active=True),

    ],
    brand="Glance",
    brand_href="/pages/home",
    color="primary",
    dark=True,
)


