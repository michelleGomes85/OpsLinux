import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests

# Registra a página no Dash com um path_template dinâmico
dash.register_page(__name__, path_template="/doc/<file_name>")

# Função para buscar o conteúdo do endpoint
def fetch_content_from_endpoint(file_name):
    url = f"http://127.0.0.1:5000/api/docs/{file_name}" 
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Erro ao carregar o conteúdo: {e}"

# Layout da página
def layout(file_name=None):
    
    if file_name is None:
        return html.Div("Nenhum arquivo selecionado.")
    
    # Carrega o conteúdo do endpoint
    content = fetch_content_from_endpoint(file_name)
    
    # Exibe o conteúdo
    return html.Div([
        dcc.Markdown(content, className="markdown-content")
    ], className="doc-content")