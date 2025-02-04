from flask import Blueprint
from .cpu import cpu_bp
from .disk import disk_bp
from .memory import memory_bp
from .network import network_bp
from .processes import processes_bp
from .uptime import uptime_bp
from .system_info import system_info_bp
from .docs import docs_bp

# api/routes/__init__.py

from .cpu import cpu_bp
from .disk import disk_bp
from .memory import memory_bp
from .network import network_bp
from .processes import processes_bp
from .uptime import uptime_bp
from .system_info import system_info_bp

# Criar o Blueprint principal da API
api_bp = Blueprint("api", __name__)

# Registrar os endpoints
api_bp.register_blueprint(cpu_bp, url_prefix='/cpu')
api_bp.register_blueprint(disk_bp, url_prefix='/disk')
api_bp.register_blueprint(memory_bp, url_prefix='/memory')
api_bp.register_blueprint(network_bp, url_prefix='/network')
api_bp.register_blueprint(processes_bp, url_prefix='/processes')
api_bp.register_blueprint(uptime_bp, url_prefix='/uptime')
api_bp.register_blueprint(system_info_bp, url_prefix='/system-info')

# Registrar os endpoints de documentação
api_bp.register_blueprint(docs_bp, url_prefix='/docs')
