from flask import Blueprint, jsonify

uptime_bp = Blueprint('uptime', __name__)

"""

Aqui está a documentação para a rota /uptime:

Endpoint: /uptime
Método: GET

Descrição: Retorna o tempo de atividade do sistema em segundos, minutos e horas.

Exemplo de Resposta:

'''json
{
    "uptime_seconds": 123456.78,
    "uptime_minutes": 2057.61,
    "uptime_hours": 34.29
}
'''

Uso Esperado:

Essa rota pode ser usada para obter o tempo de atividade de uma máquina Linux e exibir essa informação ao usuário.

"""

@uptime_bp.route('/', methods=['GET'])
def get_uptime():

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    
    uptime_minutes = uptime_seconds / 60
    uptime_hours = uptime_seconds / 3600

    return jsonify({
        'uptime_seconds': uptime_seconds,
        'uptime_minutes': uptime_minutes,
        'uptime_hours': uptime_hours
    })
