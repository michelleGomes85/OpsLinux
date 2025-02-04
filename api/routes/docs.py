# api/routes/docs.py

import os
from flask import Blueprint, send_from_directory

docs_bp = Blueprint("docs", __name__)

# Rota para acessar a documentação dos endpoints em formato markdown
@docs_bp.route("/<endpoint>")
def serve_doc(endpoint):
    try:
        # Definir o caminho dos arquivos .md
        doc_path = os.path.join(os.path.dirname(__file__), "..", "docs", f"{endpoint}.md")
        return send_from_directory(os.path.dirname(doc_path), f"{endpoint}.md")
    except FileNotFoundError:
        return "Documentação não encontrada para esse endpoint", 404
