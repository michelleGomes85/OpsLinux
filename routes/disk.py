from flask import Blueprint, jsonify
import psutil

disk_bp = Blueprint('disk', __name__)

"""

Aqui está a documentação para a rota /disk:

Endpoint: /disk
Método: GET

Descrição: Retorna informações úteis sobre o espaço em disco, incluindo o total, usado, livre e a porcentagem de uso.

Exemplo de Resposta:

'''json
{
    "total_space_gb": 500.11,
    "used_space_gb": 250.34,
    "free_space_gb": 249.77,
    "percent_used": 50.1
}
'''

Uso Esperado:

Essa rota pode ser usada para monitorar o uso do disco, identificando quando o espaço livre está baixo e evitando problemas de armazenamento.

"""

@disk_bp.route('/', methods=['GET'])
def get_disk_info():

    disk = psutil.disk_usage('/')
    total_space_gb = disk.total / (1024**3)
    used_space_gb = disk.used / (1024**3)
    free_space_gb = disk.free / (1024**3)
    percent_used = disk.percent

    return jsonify({
        'total_space_gb': round(total_space_gb, 2),
        'used_space_gb': round(used_space_gb, 2),
        'free_space_gb': round(free_space_gb, 2),
        'percent_used': percent_used
    })
