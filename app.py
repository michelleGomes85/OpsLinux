from flask import Flask
from routes.uptime import uptime_bp
from routes.disk import disk_bp
from routes.network import network_bp

app = Flask(__name__)

# Registro das rotas
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(disk_bp, url_prefix='/disk')
app.register_blueprint(network_bp, url_prefix='/network')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
