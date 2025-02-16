import os
import requests
import json

from flask import Flask, request, jsonify, render_template
from datetime import datetime

from routes.cpu import cpu_bp
from routes.disk import disk_bp
from routes.memory import memory_bp
from routes.network import network_bp
from routes.processes import processes_bp
from routes.uptime import uptime_bp
from routes.system_info import system_info_bp
from routes.documentation import documentation_bp  # Importe o novo Blueprint

from utils.utils import get_documentation
from services.ai_service import first_agent

API_BASE_URL = "http://localhost:5002{endpoint}"

app = Flask(__name__)

# Registro das rotas
app.register_blueprint(cpu_bp, url_prefix='/cpu')
app.register_blueprint(disk_bp, url_prefix='/disk')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(network_bp, url_prefix='/network')
app.register_blueprint(processes_bp, url_prefix='/processes')
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(system_info_bp, url_prefix='/system-info')
app.register_blueprint(documentation_bp)  # Registre o Blueprint da documentação

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