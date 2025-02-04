from flask import Flask, send_from_directory
from api.routes import api_bp
import config.settings as settings
from services.generate_response import generate_response
from frontend.dash_app import app_dash


server = Flask(__name__)

@server.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Registrar a API com Blueprints
server.register_blueprint(api_bp, url_prefix="/api")

# Associar Dash ao Flask
app_dash.init_app(server)

# Rota para gerar resposta
server.route('/generate-response', methods=['POST'])(generate_response)

# Iniciar o servidor
if __name__ == "__main__":
    server.run(debug=settings.DEBUG, port=settings.PORT)
