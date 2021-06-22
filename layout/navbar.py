import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import base64

def select_btn_markup():
    return dbc.NavItem(
        dbc.NavLink(
            html.I(className="fa fa-plus"),
            id="open-select-modal",
            n_clicks=0
        ),
        active=True,
        className='nav-icon',
        id='open-select-wrapper',
        style={}
    )

def upload_btn_markup():
    return dbc.NavItem(
        dbc.NavLink(
            html.I(className="fa fa-upload"),
            id='upload-button',
            n_clicks=0
        ),
        active=True,
        className='nav-icon',

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
        className='nav-icon',
    )

navbar = dbc.NavbarSimple(
    children=[
        dcc.Store(id = 'is-adjusting', data = False),
        dcc.Location(id='url', refresh=False),
        adjust_btn_markup(),
        upload_btn_markup(),
        select_btn_markup()

    ],
    id='glance-nav',
    brand="Glance",
    # brand_href="/pages/home",
    color="dark",
    dark=True,
    fixed= 'top',
    className= 'transparent-navbar',
    expand='xs',
    # fluid= True,
    style= {
        'zIndex':45,
        # 'transition': 'background .1s'
    }
)


