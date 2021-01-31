import dash_bootstrap_components as dbc
import dash_core_components as dcc

navbar = dbc.NavbarSimple(
    children=[
        dcc.Location(id='url', refresh=False),
        dbc.NavItem(dbc.NavLink("Home", href="/pages/home"),active=True),
        dbc.NavItem(dbc.NavLink("SingleView", href="/pages/singleView"), active=True),
        dbc.NavItem(dbc.NavLink("Multiview", href="/pages/carousel"), active=True),

        # dbc.DropdownMenu(
        #     children=[
        #         dbc.DropdownMenuItem("Single View", href='/pages/singleView'),
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="Glance",
    brand_href="/pages/home",
    color="primary",
    dark=True,
)