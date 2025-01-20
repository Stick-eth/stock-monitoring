import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify
from dash import Input, Output, State, callback

color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch", style={"align-self": "center"}),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-2", persistence=True, style={"align-self": "center"}),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ],
    className="d-flex justify-content-center align-items-center"
)

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo + titre (reste toujours visible)
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

                # Bouton "hamburger" visible sur mobiles
                dbc.NavbarToggler(id="navbar-toggler"),

                # Tout ce qui doit se replier sur petits écrans
                dbc.Collapse(
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

                            # Switch clair/sombre
                            color_mode_switch,

                            html.Div(style={"width": "40px"}),

                            # Icône de profil
                            html.A(
                                DashIconify(icon="healthicons:ui-user-profile", width=30, height=30, color="white"),
                                href="/profile",
                                style={"textDecoration": "none", "align-self": "center"},
                            ),
                        ],
                        className="ms-auto",  # pousse la liste d'items vers la droite
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,   # fermé par défaut
                    navbar=True,
                ),
            ]
        ),
        color="primary",
        dark=True,
    )

@callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open