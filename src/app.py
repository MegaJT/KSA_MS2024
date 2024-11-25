import dash
from dash import Dash, html, dcc, page_registry, page_container
import dash_bootstrap_components as dbc

from config import box_shadow
from config import box_shadow_rounded_corner
from config import chart_bg_space_style


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
server=app.server
app.config.suppress_callback_exceptions = True

navbar1 = dbc.NavbarSimple(
    brand="SALES",
    brand_href="/",
    color="secondary",  # Sets the background color (Bootstrap color class)
    dark=True,  # Makes the text light for dark backgrounds
    children=[
        #dbc.NavLink("OVERALL", href="/", active="exact"),
        dbc.NavLink("BRANCH", href="/S_Branch_Evaluation", active="exact"),
        dbc.NavLink("CALL CENTER", href="/S_Call_center", active="exact"),
        dbc.NavLink("WEBSITE", href="/S_Website", active="exact"),
        dbc.NavLink("ONLINE", href="/S_Online", active="exact"),
        dbc.NavLink("SM", href="/S_SM", active="exact"),
    ],
style=box_shadow_rounded_corner)

navbar2 = dbc.NavbarSimple(
    brand="AFTER SALES",
    brand_href="/",
    color="secondary",  # Sets the background color (Bootstrap color class)
    dark=True,  # Makes the text light for dark backgrounds
    children=[
        dbc.NavLink("SERVICE CENTER", href="/AS_Service_Center", active="exact"),
        dbc.NavLink("CALL CENTER", href="/AS_Call_center", active="exact"),
        dbc.NavLink("WEBSITE", href="/AS_WB", active="exact"),
        dbc.NavLink("ONLINE", href="/AS_Online", active="exact"),
        dbc.NavLink("SM", href="/AS_SM", active="exact"),
        
    ],
style=box_shadow_rounded_corner)



# Layout for app
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dbc.Row([
            dbc.Col([html.Img(src='assets/DG_Logo.jpg', height="100px")], width=2),
            dbc.Col([html.H1("")], width=2),
            dbc.Col([html.H1("MYSTERY SHOPPING -  KSA")], width=5),
            dbc.Col([html.H1("")], width=2),
            dbc.Col([html.H1("")], width=2),
            #dbc.Col([html.Img(src='assets/DG_Logo.png', height="75px",style={"float": "right"})], width=2),
        ]),
        dbc.Row([html.Hr()]),
    ]),
    
    html.Div([  navbar1,
                navbar2,
            ]),
    html.Div([html.Hr()]),
    html.Div(page_container),  # Will contain page layouts

], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True)



# ksa-ms2024-o1on.onrender.com/