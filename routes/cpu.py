import psutil
from flask import Flask, Blueprint, jsonify

cpu_bp = Blueprint('cpu', __name__)

"""

# CPU 

Endpoint: /cpu
Método: GET

Descrição: Retorna informações sobre o processador do sistema, incluindo o número de núcleos, o uso da CPU por núcleo, a frequência atual, mínima e máxima da CPU, e a temperatura (caso seja suportado pelo hardware).


Exemplo de Resposta:

'''json
{
    "cpu_count": 8,
    "cpu_usage_per_core": [15.0, 20.5, 10.0, 30.0, 25.5, 40.0, 18.0, 12.0],
    "cpu_frequency": {
        "current": 2600.0,
        "min": 800.0,
        "max": 3200.0
    },
    "cpu_temperatures": [
        {"label": "Core 0", "current": 45.0, "high": 70.0, "critical": 85.0},
        {"label": "Core 1", "current": 47.0, "high": 70.0, "critical": 85.0}
    ]
}
'''

Uso Esperado:

Essa rota pode ser utilizada para monitorar o desempenho da CPU, identificar problemas de sobrecarga e verificar as temperaturas dos núcleos do processador.

"""
@cpu_bp.route('/', methods=['GET'])
def get_cpu_info():

    cpu_count = psutil.cpu_count(logical=True)
    
    # Inicializa a medição (ignora o resultado) -> Usada para ter um resultado mais preciso
    psutil.cpu_percent(interval=0.1)
    
    # Uso da CPU por núcleo (com intervalo de 0.1 segundos)
    cpu_usage = psutil.cpu_percent(interval=0.1, percpu=True)

    cpu_frequency = psutil.cpu_freq()

    # Obtendo temperaturas (se suportado pelo hardware)
    sensors_temperatures = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
    cpu_temperatures = sensors_temperatures.get('coretemp', [])

    return jsonify({
        "cpu_count": cpu_count,
        "cpu_usage_per_core": cpu_usage,
        "cpu_frequency": {
            "current": cpu_frequency.current if cpu_frequency else None,
            "min": cpu_frequency.min if cpu_frequency else None,
            "max": cpu_frequency.max if cpu_frequency else None
        },
        "cpu_temperatures": [
            {"label": temp.label, "current": temp.current, "high": temp.high, "critical": temp.critical}
            for temp in cpu_temperatures
        ]
    })
