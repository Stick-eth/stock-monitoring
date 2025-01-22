from dash import html, dcc

def privacy_policy_layout():
    """
    Layout of the 'Privacy Policy' page.
    """
    return html.Div([
    # Title
    html.H1("Privacy Policy", style={'textAlign': 'center', 'marginTop': '20px'}),
    # Last updated date
    html.P("Last Updated: 22/01/2025", style={'textAlign': 'center', 'fontStyle': 'italic'}),
    
    # Introduction
    html.Div([
        html.P("Welcome to DataStick! Your privacy is important to us. This Privacy Policy outlines how we collect, use, and protect your information when you use our web application."),
    ], style={'width': '60%', 'margin': '40px auto', 'lineHeight': '1.6'}),
    
    # Information We Collect
    html.H2("1. Information We Collect"),
    html.Ul([
        html.Li("Personal Information: If you sign up or contact us, we may collect your name, email address, and other relevant details."),
        html.Li("Usage Data: Information about how you interact with the application, including your searches, preferences, and activities within DataStick."),
        html.Li("Cookies and Tracking Technologies: We use cookies to improve user experience and analyze app performance."),
    ]),
    
    # How We Use Your Information
    html.H2("2. How We Use Your Information"),
    html.Ul([
        html.Li("Provide and improve the services offered by DataStick."),
        html.Li("Personalize your experience and optimize the user interface."),
        html.Li("Analyze trends and monitor app usage for performance enhancement."),
        html.Li("Respond to inquiries or support requests."),
    ]),
    html.P("We do not sell, trade, or rent your personal information to third parties."),
    
    # Data Security
    html.H2("3. Data Security"),
    html.P("We implement appropriate security measures to protect your personal data from unauthorized access, alteration, or disclosure. However, no method of transmission over the internet is 100% secure, and we cannot guarantee absolute security."),
    
    # Third-Party Services
    html.H2("4. Third-Party Services"),
    html.P("DataStick may integrate with third-party APIs (e.g., financial data providers). These services have their own privacy policies, and we encourage you to review them."),
    
    # Your Rights & Choices
    html.H2("5. Your Rights & Choices"),
    html.Ul([
        html.Li("Access, update, or delete your personal data."),
        html.Li("Opt-out of tracking or cookie usage through your browser settings."),
        html.Li("Contact us regarding any privacy concerns."),
    ]),
    
    # Changes to This Policy
    html.H2("6. Changes to This Policy"),
    html.P("We may update this Privacy Policy from time to time. Any changes will be reflected on this page with an updated 'Last Updated' date."),
    
    # Contact Information
    html.H2("7. Contact Information"),
    html.P("For any questions regarding this Privacy Policy, please contact us at:"),
    html.P("Email: contact@datastick.com", style={'fontWeight': 'bold'}),
    
    # Thank You Message
    html.P("Thank you for using DataStick!", style={'textAlign': 'center', 'marginTop': '20px'})
], style={'width': '60%', 'margin': '40px auto', 'lineHeight': '1.6'})