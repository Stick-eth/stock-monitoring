from dash import html
import dash_bootstrap_components as dbc

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
                        dbc.NavItem(dbc.NavLink("Accueil", href="/")),
                        dbc.NavItem(dbc.NavLink("Stocks", href="/stocks/", external_link=True)),
                        dbc.NavItem(dbc.NavLink("À propos", href="/about")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                color_mode_switch,
            ]
        ),
        color="primary",
        dark=True,
    )
