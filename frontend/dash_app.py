import dash
from dash import html
from dash import dcc
from dash import Input, Output
import dash_bootstrap_components as dbc

from frontend.dashboard_layout import dashboard_layout
from frontend.layout import doc_layout

app_dash = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.10.5/font/bootstrap-icons.min.css",
        "https://fonts.googleapis.com/icon?family=Material+Icons",
        "/static/css/styles.css",
        "/static/css/styles_doc.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
    ],
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js",
        "/static/js/script.js"
    ]
)

app_dash.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    html.Div(id='page-content')  
])

@app_dash.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    if pathname == '/':
        return dashboard_layout
    elif pathname.startswith('/doc'):
        return doc_layout
    else:
        return html.Div([html.H3('404 - Página não encontrada')])
    
    
    