from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ],className="ml-4",
)

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/logo.png", height="40px")),
                            dbc.Col(dbc.NavbarBrand("DataStick", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/")),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Stocks", href="/stocks/", external_link=True),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Screener",
                        ),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("Manage", header=True),
                                dbc.DropdownMenuItem("Overview", href="#"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Portfolio",
                        ),
                        dbc.NavItem(dbc.NavLink("À propos", href="/about")),
                        html.Div(style={"width": "40px"}),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                color_mode_switch,
                html.Div(style={"width": "40px"}),
                html.A(
                    DashIconify(icon="healthicons:ui-user-profile", width=30, height=30, color="primary"),
                    href="/login"
                ),
            ]
        ),
        color="primary",
        dark=True,
    )
