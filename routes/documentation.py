from flask import Blueprint, render_template
import os
from datetime import datetime

documentation_bp = Blueprint('documentation', __name__)

PROJECT_INFO = {
    "name": "OpsLinux",
    "version": "0.0.4",
    "authors": [
        {"name": "Gabriel Barbosa", "github": "https://github.com/GabrielBarbosaAfo"},
        {"name": "Michelle Gomes", "github": "https://github.com/michelleGomes85"}
    ],
    "last_modified": datetime.now().strftime("%d/%m/%Y"),
    "gitrepo": "https://github.com/michelleGomes85/OpsLinux",
}

@documentation_bp.route('/doc')
def documentation():
    doc_files = sorted([f for f in os.listdir('docs') if f.endswith('.md')])
    return render_template('documentation.html', project=PROJECT_INFO, doc_files=doc_files)

@documentation_bp.route('/doc/<filename>')
def show_doc(filename):
    filepath = os.path.join('docs', filename)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content