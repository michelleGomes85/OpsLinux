import dash
from dash import html

dash.register_page(__name__, path_template="/doc")

def layout(file_name=None):

    return html.Div([

        html.Link(
            rel='stylesheet',
            href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
        ),
        
        html.H1(
            children=[
                html.Span("OpsLinux", className="apresentation"),
                " API Documentação"
            ]
        ),
        html.P([
            "A ", html.Strong("OpsLinuxAPI"), 
            " é uma API projetada para monitorar e obter informações detalhadas sobre o sistema Linux. "
            "Ela oferece dados em tempo real sobre o uso de CPU, memória, discos, interfaces de rede, "
            "processos em execução e tempo de atividade do sistema."
        ]),
        
        html.Div(
            children=[
                html.P("Construída com:"),
                html.Div(
                    children=[
                        html.I(className="fab fa-python"),
                        html.I(className="fas fa-fire")
                    ],
                    className="technologies"
                ),
                html.Div(
                    children=[
                        html.Span("Python"),
                        html.Span("Flask")
                    ],
                    className="tech-labels"
                )
            ],
            className="built-with center-align",
            style={"marginTop": "40px"}
        ),
        
        html.P(
            "No menu acima ou ao lado se estiver no celular, você encontrará links para descrições detalhadas de "
            "cada módulo da API, permitindo explorar todas as funcionalidades disponíveis de maneira fácil e organizada."
        )
    ], className="doc-content")
