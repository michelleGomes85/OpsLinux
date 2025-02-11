from datetime import datetime, timedelta
from flask import Blueprint, jsonify
import psutil
import platform

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
    try:
        # Verifica o sistema operacional
        system_os = platform.system().lower()

        if system_os == "linux":
            # Lógica para Linux
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
        elif system_os == "windows":
            # Lógica para Windows
            uptime_seconds = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - uptime_seconds
        else:
            return jsonify({"error": "Sistema operacional não suportado"}), 500

        # Calcular minutos, horas e dias
        uptime_minutes = uptime_seconds / 60
        uptime_hours = uptime_seconds / 3600
        uptime_days = uptime_seconds / 86400

        # Formatar o tempo de atividade em uma string legível
        uptime_formatted = str(timedelta(seconds=int(uptime_seconds)))

        # Calcular a data e hora de inicialização
        boot_time = datetime.now() - timedelta(seconds=uptime_seconds)

        # Verificar se o sistema foi reiniciado recentemente
        recently_rebooted = uptime_seconds < 60  # Menos de 1 minuto

        return jsonify({
            'uptime_seconds': uptime_seconds,
            'uptime_minutes': uptime_minutes,
            'uptime_hours': uptime_hours,
            'uptime_days': uptime_days,
            'uptime_formatted': uptime_formatted,
            'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
            'recently_rebooted': recently_rebooted
        })

    except FileNotFoundError:
        return jsonify({"error": "Arquivo /proc/uptime não encontrado (sistema não suportado)"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500