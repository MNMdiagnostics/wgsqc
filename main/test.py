import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dashboard = dbc.Navbar(
    [
        dbc.Col(dbc.NavbarBrand("Dashboard", href="#"), sm=3, md=2),
        dbc.Col(dbc.Input(type="search", placeholder="Search here")),
        dbc.Col(
            dbc.Nav(dbc.NavItem(dbc.NavLink("Sign out")), navbar=True),
            width="auto",
        ),
    ],
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [dashboard]
)
if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

