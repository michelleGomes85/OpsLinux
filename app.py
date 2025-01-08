from flask import Flask
from routes.uptime import uptime_bp
from routes.cpu import cpu_bp
from routes.memory import memory_bp
from routes.processes import processes_bp

app = Flask(__name__)

# Registro das rotas
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(cpu_bp, url_prefix='/cpu')
app.register_blueprint(memory_bp, url_prefix='/memory')
app.register_blueprint(processes_bp, url_prefix='/processes')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
