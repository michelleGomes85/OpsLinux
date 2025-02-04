import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import requests

dash.register_page(__name__, path="/")

def fetch_system_info():
    try:
        response = requests.get("http://127.0.0.1:5000/api/system-info/", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None

def create_button_section():
    return html.Div([
        html.P(
            children=[
                "Monitore seu sistema em ",
                html.Span("tempo real ", className="highlight"),
                "com ",
                html.Span("IA", className="highlight"),
                ".",
                html.Br(),
                "Clique e faça ",
                html.Span("perguntas", className="highlight"),
                " sobre o status completo."
            ],
            className="subtitle"
        ),
        html.Div([
            html.A(
                children=[
                    html.I(className="material-icons left", children="help_outline"),
                    "Faça uma pergunta"
                ],
                className="waves-effect waves-light btn btn-question", href="#modal-question"
            ),
        ], id="open-modal-btn", className="button-section")
    ], className="banner")

def create_ip_section(ip_address):
    return html.Div([
        html.I(className="fas fa-sync-alt", id="ip-toggle-icon"),
        html.Div([
            html.Div([
                html.P(id="ip-display-ip-text", children="IPV4"),
            ]),

            html.Div([
                html.P(id="ip-display-ipv4", children=f"{ip_address.get('ipv4', 'N/A')}"),
                html.P(id="ip-display-ipv6", children=f"{ip_address.get('ipv6', 'N/A')}"),
            ]),
        ], className="ip-div")
    ], className="ip-section", id="ip-section")

def create_uptime_section(uptime_seconds):
    return html.Div([
        html.Div([
            html.Div(className="donut", id="donut")
        ], className="chart-container"),

        html.P(id="uptime-display", children="Carregando...", **{"data-uptime": uptime_seconds}),
    ], className="uptime-section")

def create_graph_section():
    return html.Div([
        html.Div([
            html.Div([dcc.Graph(id='memory-graph')], className="memory-section"),
            html.Div([dcc.Graph(id='disk-graph')], className="disk-section"),
        ], className="memory-disk-container"),
        
        html.Div([
            dcc.Graph(id='cpu-graph'),
        ], className="cpu-section"),
    ], className="graphs-section")

import dash
from dash import html, dcc

def createModalQuestion():

    return html.Div([

        html.Div([  # Modal Content
            html.Div([  # Ícones de Perguntas
                html.Div([
                    html.Div([
                        html.A(
                            html.I("memory", className="material-icons"),
                            className="icon-link tooltipped",
                            **{"data-question": "Qual é o uso atual da CPU?", "data-tooltip": "Perguntar sobre CPU"}
                        )
                    ]),

                    html.Div([
                        html.A(
                            html.I("storage", className="material-icons"),
                            className="icon-link tooltipped",
                            **{"data-question": "Qual é o espaço livre no disco?", "data-tooltip": "Perguntar sobre Disco"}
                        )
                    ]),

                    html.Div([
                        html.A(
                            html.I("sd_card", className="material-icons"),
                            className="icon-link tooltipped",
                            **{"data-question": "Qual é o uso atual da memória?", "data-tooltip": "Perguntar sobre Memória"}
                        )
                    ]),

                    html.Div([
                        html.A(
                            html.I("delete", className="material-icons"),
                            className="icon-link tooltipped",
                            id="clear-question",
                            **{"data-tooltip": "Limpar caixa de texto"}
                        )
                    ]),
                ], className="text-questions")
            ], className="icons-question"),

            html.Div([  # Caixa de Texto e Microfone
                dcc.Textarea(
                    id="question",
                    placeholder="Faça uma pergunta sobre o sistema...",
                    className="materialize-textarea bg-dark text-light"
                ),

                html.Div([
                    html.Span(
                        html.I("mic", className="material-icons"),
                        id="microphone",
                        className="microphone-icon"
                    )
                ], id="microphone-container"),
            ], className="input-field mt-4"),

            html.Div([  # Efeito de Carregamento
                html.Div(className="loading-bar"),
            ], id="loadingEffect", className="loading-effect", style={"display": "none"}),

            html.Div([  # Rodapé do Modal
                html.A("Fechar", href="#!", className="modal-close waves-effect waves-green btn-flat text-success"),
                html.A("Enviar", href="#!", id="send-question", className="waves-effect waves-green btn-flat text-success"),
            ], className="modal-footer bg-dark"),

        ], className="modal-content bg-dark text-light"),

    ], id="modal-question", className="modal")

def layout():
    system_info = fetch_system_info()
    
    if not system_info:
        return html.Div("Erro ao carregar dados do sistema.")
    
    ip_address = system_info.get("ip_address", {})
    uptime_seconds = system_info.get("uptime", {}).get("seconds", 0)
    
    button_section = create_button_section()
    ip_section = create_ip_section(ip_address)
    uptime_section = create_uptime_section(uptime_seconds)
    graph_section = create_graph_section()
    modal = createModalQuestion()
    
    return html.Div([
        modal,
        html.Link(rel="stylesheet", href="/static/css/styles_dashboard.css"),
        button_section,

        html.Div([
            ip_section,
            uptime_section
        ], className="ip-time"),

        dcc.Store(id="uptime-store", data={"seconds": uptime_seconds}),
        graph_section,
    ], className="content-result")