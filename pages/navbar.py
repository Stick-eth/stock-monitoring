from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/logo.png", height="40px")),
                            dbc.Col(dbc.NavbarBrand("Stock Monitoring", className="ms-2")),
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
                        dbc.NavItem(dbc.NavLink("Stocks", href="/stocks")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
    )
