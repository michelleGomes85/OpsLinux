import os
import markdown
import requests
import json

from flask import Flask
from flask import Flask, send_from_directory
from datetime import datetime
from flask import request
from flask import Flask, render_template, abort
from flask import jsonify

from routes.cpu import cpu_bp
from routes.disk import disk_bp
from routes.memory import memory_bp
from routes.network import network_bp
from routes.processes import processes_bp
from routes.uptime import uptime_bp
from routes.system_info import system_info_bp

from utils.utils import get_documentation
from services.ai_service import first_agent

API_BASE_URL = "http://localhost:5002{endpoint}"

app = Flask(__name__)

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

# Registro das rotas
app.register_blueprint(cpu_bp, url_prefix='/cpu')
app.register_blueprint(disk_bp, url_prefix='/disk')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(network_bp, url_prefix='/network')
app.register_blueprint(processes_bp, url_prefix='/processes')
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(system_info_bp, url_prefix='/system-info')

# Rota principal da documentação
@app.route('/doc')
def documentation():

    doc_files = sorted([f for f in os.listdir('docs') if f.endswith('.md')])

    return render_template('documentation.html', project=PROJECT_INFO, doc_files=doc_files)

# Rota para exibir um arquivo Markdown específico (para AJAX)
@app.route('/doc/<filename>')
def show_doc(filename):
    
    filepath = os.path.join('docs', filename)
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-response', methods=['POST'])
def generate_response():
    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400 

        documentation = get_documentation()

        prompt =  f'''
        
        analise cuidadosamente a seguinte documentação:  {documentation}  

        Com base nessa análise, determine quais endpoints são necessários para responder à seguinte pergunta:  "{question}"  

        Se a pergunta fizer sentido com a documentação disponível, forneça a resposta no seguinte formato JSON:  

        {{
            "endpoints": ["endpoint1", "endpoint2", ...],
            "error": null
        }}

        Caso a pergunta **não tenha relação** com a documentação, retorne um JSON com uma explicação bem-humorada e um trocadilho com Linux sobre o motivo da informação não existir. Exemplo:  

        {{
            "endpoints": [],
            "error": Informação não encontrada. Parece que essa pergunta fugiu do escopo, assim como processos zumbis fogem do controle no Linux."
        }}

        Certifique-se de que a resposta esteja bem formatada e estruturada conforme os exemplos acima.  

        '''

        response =  first_agent(prompt)

        response_data = {
            'response': response,
        }

        
        json_response = json.loads(response_data['response'])

        responde_teste = ""

        for e in json_response['endpoints']:
            responde_teste += json.dumps(fetch_system_info(e))
            print(responde_teste)

        prompt_second = f'''
            Considerando a seguinte infomração em JSON sobre uma máquina linux: 
            
            {responde_teste}, 
            
            Responda a seguinte pergunta: {question}. 
            
            Estruture sua resposta em linguagem natural, como o JSON a seguir:

            {{
                'question': 'Qual é o espaço livre no disco?',
                'response': "Há 32 GB de espaço livre em disco."

            }}
        '''

        response_second = first_agent(prompt_second)

        return jsonify(response_second)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    

def fetch_system_info(endpoint):
    try:
        response = requests.get(API_BASE_URL.format(endpoint=endpoint), timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None
        


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

