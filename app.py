from flask import Flask
from flask import Flask, send_from_directory
from datetime import datetime
from flask import Flask, render_template, abort

from routes.cpu import cpu_bp
from routes.disk import disk_bp
from routes.memory import memory_bp
from routes.network import network_bp
from routes.processes import processes_bp
from routes.uptime import uptime_bp

import os
import markdown

app = Flask(__name__)

PROJECT_INFO = {
    "name": "OpsLinux",
    "version": "1.0.0",
    "authors": ["Gabriel Barbosa", "Michelle Gomes"],
    "last_modified": datetime.now().strftime("%d/%m/%Y"),
}

# Rota principal da documentação
@app.route('/doc')
def documentation():
    doc_files = sorted([f for f in os.listdir('docs') if f.endswith('.md')])
    return render_template('documentation.html', project=PROJECT_INFO, doc_files=doc_files)

# Rota para exibir um arquivo Markdown específico (para AJAX)
@app.route('/doc/<filename>')
def show_doc(filename):
    filepath = os.path.join('docs', filename)
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
    return html_content

# Registro das rotas
app.register_blueprint(cpu_bp, url_prefix='/cpu')
app.register_blueprint(disk_bp, url_prefix='/disk')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(network_bp, url_prefix='/network')
app.register_blueprint(processes_bp, url_prefix='/processes')
app.register_blueprint(uptime_bp, url_prefix='/uptime')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
