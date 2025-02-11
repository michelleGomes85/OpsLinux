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
    cpu_physical_count = psutil.cpu_count(logical=False)  # Número de núcleos físicos
    
    # Inicializa a medição (ignora o resultado) -> Usada para ter um resultado mais preciso
    psutil.cpu_percent(interval=0.1)
    
    # Uso da CPU por núcleo (com intervalo de 0.1 segundos)
    cpu_usage_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_usage_total = psutil.cpu_percent(interval=0.1)  # Uso total da CPU

    # Frequência da CPU
    cpu_frequency = psutil.cpu_freq()

    # Tempos de execução da CPU
    cpu_times = psutil.cpu_times()
    cpu_times_percent = psutil.cpu_times_percent(interval=0.1)

    # Informações sobre a CPU
    cpu_info = psutil.cpu_info() if hasattr(psutil, "cpu_info") else {}

    # Obtendo temperaturas (se suportado pelo hardware)
    sensors_temperatures = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
    cpu_temperatures = sensors_temperatures.get('coretemp', [])

    # Carga média do sistema (apenas no Linux)
    load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else None

    return jsonify({
        "cpu_count": cpu_count,
        "cpu_physical_count": cpu_physical_count,
        "cpu_usage_per_core": cpu_usage_per_core,
        "cpu_usage_total": cpu_usage_total,
        "cpu_frequency": {
            "current": cpu_frequency.current if cpu_frequency else None,
            "min": cpu_frequency.min if cpu_frequency else None,
            "max": cpu_frequency.max if cpu_frequency else None
        },
        "cpu_times": {
            "user": cpu_times.user,
            "system": cpu_times.system,
            "idle": cpu_times.idle,
            "iowait": getattr(cpu_times, 'iowait', None)  # Pode não estar disponível em todos os sistemas
        },
        "cpu_times_percent": {
            "user": cpu_times_percent.user,
            "system": cpu_times_percent.system,
            "idle": cpu_times_percent.idle,
            "iowait": getattr(cpu_times_percent, 'iowait', None)  # Pode não estar disponível em todos os sistemas
        },
        "cpu_info": {
            "brand": cpu_info.get('brand_raw', 'N/A'),
            "arch": cpu_info.get('arch', 'N/A'),
            "bits": cpu_info.get('bits', 'N/A'),
            "cores": cpu_info.get('cores', 'N/A'),
            "threads": cpu_info.get('threads', 'N/A')
        },
        "cpu_temperatures": [
            {"label": temp.label, "current": temp.current, "high": temp.high, "critical": temp.critical}
            for temp in cpu_temperatures
        ],
        "load_avg": load_avg if load_avg else None
    })
