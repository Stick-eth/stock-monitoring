from dash import html, dcc

def about_layout():
    """Layout de la page 'À Propos' avec texte et CV en anglais."""
    return html.Div([
        # Introduction et présentation
        html.H1("About", style={'textAlign': 'center', 'marginTop': '20px'}),
        html.Div([
            html.P(
                    "📊 DataStick is a web application designed to simplify financial analysis for publicly traded companies. "
                    "It provides an intuitive interface for exploring financial data, bridging the gap between accessibility and professional-grade insights."
                ),
                html.P(
                    "👷Developed during my free time, DataStick is both a tool to democratize financial information and a personal project to enhance my expertise in data visualization and analysis."
                ),
                html.P(
                    "👋 I'm Aniss, an IT engineering student with a deep interest in empowering informed investment decisions through technology and data-driven solutions."
                )
        ], style={'width': '60%', 'margin': '40px auto', 'lineHeight': '1.6'}),

        # Ajout du CV en markdown (anglais)
        html.Div([
            html.A(
                'View my portfolio',
                href='https://aniss-sej.notion.site',
                style={'fontSize': '20px', 'textDecoration': 'none'}
            )
        ], style={'display': 'flex', 'justifyContent': 'center'}),

        # Ajout d'un diviseur
        html.Div(style={'borderTop': '1px solid #ccc', 'marginTop': '40px', 'marginLeft': '20%', 'marginRight': '20%'}),
        # Link to the privacy policy page
        html.Div([
            html.A(
                'Privacy Policy',
                href='/privacy',
                style={'fontSize': '20px', 'textDecoration': 'none'}
            )
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'}),
    ])
