import os
import dash
from dash import html, page_container
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
from config.settings import PROJECT_INFO
from dash import callback_context

DOCS_FOLDER = "api/docs"

def list_markdown_files():
    return [f.replace(".md", "") for f in os.listdir(DOCS_FOLDER) if f.endswith(".md")]

doc_layout = html.Main([

    # Cabeçalho
    html.Header([
        html.Img(src="/assets/logo.png", className="logo", alt="Logo OpsLinux"),
        html.Span("OpsLinux")
    ], className="navbar"),

    # Layout principal
    html.Section([

        # Barra lateral (nav)
        html.Aside([
            html.Span(className="span-space"),
            html.Nav([
                html.A([
                    html.I(className="bi bi-bar-chart"),
                    html.Span("Dashboard", className="tooltip-text")
                ], href="/", className="sidebar-item"),

                html.A([
                    html.I(className="bi bi-file-earmark-text"),
                    html.Span("Docs", className="tooltip-text")
                ], href="/doc", className="sidebar-item item-doc"),

                html.A([
                    html.I(className="bi bi-info-circle"),
                    html.Span("Info", className="tooltip-text")
                ], href="#", className="sidebar-item"),
            ], className="sidebar")
        ]),

        # Conteúdo dinâmico baseado na página acessada
        html.Article([
            # Menu de links fixo na parte superior
            html.Div(id="doc-menu", children=[
                dcc.Link('home', href='/doc'),
                *[
                    dcc.Link(f"{file}", href=f"/doc/{file}", className="links-end") 
                    for file in list_markdown_files()
                ]
            ]),

            page_container

        ], className="content"),

        # Botão Fixo
        html.Div(className="fixed-action-btn", children=[
            html.A(
                className="btn-floating btn-large waves-effect waves-light bg-success",
                id="open-modal-btn",
                children=[html.I(className="material-icons", children="info")]
            )
        ]),

        # Modal
        dbc.Modal(
            [
                dbc.ModalHeader(f"Sobre o {PROJECT_INFO['name']}"),
                dbc.ModalBody([
                    
                    # Versão
                    html.Div([
                        html.Span(f"Versão: {PROJECT_INFO['version']}")
                    ], style={"marginBottom": "10px"}),

                    # Autores
                    html.Div([
                        html.Span("Autores: "),
                        html.Div(
                            children=[
                                html.A(
                                    author["name"],
                                    href=author["github"],
                                    target="_blank",
                                    style={"marginRight": "10px"}
                                ) for author in PROJECT_INFO['authors']
                            ],
                            style={"display": "inline-block"}
                        ),
                    ], style={"marginBottom": "10px"}), 

                    # Repositório
                    html.Div([
                        html.Span("Repositório: "),
                        html.Span(
                            html.A(
                                "GitHub",
                                href=PROJECT_INFO["gitrepo"],
                                target="_blank"
                            ),
                            style={"display": "inline-block"}
                        ),
                    ], style={"marginBottom": "10px"}),

                    # Última Atualização
                    html.Div([
                        html.P(f"Última Atualização: {PROJECT_INFO['last_modified']}")
                    ]),

                ]),
                dbc.ModalFooter(
                    dbc.Button("Fechar", id="close-modal-btn", className="btn btn-secondary")
                ),
            ],
            id="infoModal",
            is_open=False,
        ),

    ], className="main-content")
])

@dash.callback (
    dash.dependencies.Output('doc-menu', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)

def update_active_link(pathname):

    home_active = 'active-link' if pathname == '/doc' or pathname == '/' else 'links-end'

    links = [
        dcc.Link('home', href='/doc', className=home_active),
        *[
            dcc.Link(f"{file}", href=f"/doc/{file}", className="links-end" if f"/doc/{file}" not in pathname else 'active-link')
            for file in list_markdown_files()
        ]
    ]

    return links

@dash.callback(
    Output('infoModal', 'is_open'),
    [Input('open-modal-btn', 'n_clicks'), Input('close-modal-btn', 'n_clicks')],
    [dash.dependencies.State('infoModal', 'is_open')]
)

def toggle_modal(open_clicks, close_clicks, is_open):
    
    ctx = callback_context 
    if not ctx.triggered:
        return is_open  

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "open-modal-btn":
        return True
    elif button_id == "close-modal-btn":
        return False

    return is_open  
