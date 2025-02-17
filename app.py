
from flask import Flask, render_template

from api.routes.cpu import cpu_bp
from api.routes.disk import disk_bp
from api.routes.memory import memory_bp
from api.routes.network import network_bp
from api.routes.processes import processes_bp
from api.routes.uptime import uptime_bp
from api.routes.system_info import system_info_bp
from services.documentation import documentation_bp

from services.generate_response import generate_response

app = Flask(__name__)

# Registro das rotas

# Rota para o endpoints
app.register_blueprint(cpu_bp, url_prefix='/cpu')
app.register_blueprint(disk_bp, url_prefix='/disk')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(network_bp, url_prefix='/network')
app.register_blueprint(processes_bp, url_prefix='/processes')
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(system_info_bp, url_prefix='/system-info')

# Rota para a documentação
app.register_blueprint(documentation_bp) 

# Rota para gerar resposta
app.route('/generate-response', methods=['POST'])(generate_response)

@app.route('/')
def index():
    return render_template('dashboard.html')
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)