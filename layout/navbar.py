import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import base64

def upload_btn_markup():
    return dbc.NavItem(
        dbc.NavLink(
            html.I(className="fa fa-upload"),
            id='upload-button',
            n_clicks=0
        ),
        active=True,
        className='nav-icon'
    )

def adjust_btn_markup():
    return dbc.NavItem(
        dbc.NavLink(
            html.I(className="fa fa-arrows-alt", id='adjust-svg'),
            id='adjust-button',
            n_clicks=0
        ),
        active=True,
        id = 'adjust-wrapper',
        className='nav-icon'
    )

navbar = dbc.NavbarSimple(
    children=[
        dcc.Store(id = 'is-adjusting', data = False),
        dcc.Location(id='url', refresh=False),
        adjust_btn_markup(),
        upload_btn_markup(),

    ],
    brand="Glance",
    brand_href="/pages/home",
    color="dark",
    dark=True,
)


