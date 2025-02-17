import psutil
from flask import Flask, Blueprint, jsonify

cpu_bp = Blueprint('cpu', __name__)

"""
# CPU Monitor API

## Endpoint: `/cpu`
**Método:** GET

### Descrição:
Retorna informações detalhadas sobre o processador do sistema, incluindo:
- Número de núcleos lógicos e físicos
- Uso da CPU por núcleo e total
- Frequência mínima, máxima e atual da CPU
- Tempos de execução da CPU
- Informações gerais da CPU (se disponível)
- Temperatura da CPU (se suportado pelo hardware)
- Carga média do sistema (apenas em sistemas compatíveis)

### Exemplo de Resposta:
```json
{
    "cpu_count": 8,
    "cpu_physical_count": 4,
    "cpu_usage_per_core": [15.0, 20.5, 10.0, 30.0, 25.5, 40.0, 18.0, 12.0],
    "cpu_usage_total": 25.4,
    "cpu_frequency": {
        "current": 2600.0,
        "min": 800.0,
        "max": 3200.0
    },
    "cpu_times": {
        "user": 12345.6,
        "system": 6789.0,
        "idle": 98765.4,
        "iowait": 234.5
    },
    "cpu_times_percent": {
        "user": 30.0,
        "system": 15.0,
        "idle": 50.0,
        "iowait": 5.0
    },
    "cpu_info": {
        "brand": "Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz",
        "arch": "x86_64",
        "bits": 64,
        "cores": 4,
        "threads": 8
    },
    "cpu_temperatures": [
        {"label": "Core 0", "current": 45.0, "high": 70.0, "critical": 85.0},
        {"label": "Core 1", "current": 47.0, "high": 70.0, "critical": 85.0}
    ],
    "load_avg": [1.25, 1.10, 0.95]
}
```

### Uso:
Pode ser utilizado para monitorar o desempenho da CPU, identificar problemas de sobrecarga e verificar temperaturas dos núcleos do processador.
"""

@cpu_bp.route('/', methods=['GET'])
def get_cpu_info():
    cpu_count = psutil.cpu_count(logical=True)
    cpu_physical_count = psutil.cpu_count(logical=False)
    
    # Inicializa a medição para precisão
    psutil.cpu_percent(interval=0.1)
    
    # Coleta dados de uso da CPU
    cpu_usage_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_usage_total = psutil.cpu_percent(interval=0.1)
    
    # Frequência da CPU
    cpu_frequency = psutil.cpu_freq()
    
    # Tempos de execução da CPU
    cpu_times = psutil.cpu_times()
    cpu_times_percent = psutil.cpu_times_percent(interval=0.1)
    
    # Informações gerais da CPU (se disponível)
    cpu_info = {}  
    if hasattr(psutil, "cpu_info"):
        cpu_data = psutil.cpu_info()
        cpu_info = {
            "brand": getattr(cpu_data, 'brand_raw', 'N/A'),
            "arch": getattr(cpu_data, 'arch', 'N/A'),
            "bits": getattr(cpu_data, 'bits', 'N/A'),
            "cores": getattr(cpu_data, 'cores', 'N/A'),
            "threads": getattr(cpu_data, 'threads', 'N/A')
        }
    
    # Temperaturas da CPU (se suportado pelo hardware)
    cpu_temperatures = []
    if hasattr(psutil, "sensors_temperatures"):
        sensors_data = psutil.sensors_temperatures()
        if 'coretemp' in sensors_data:
            cpu_temperatures = [
                {"label": temp.label, "current": temp.current, "high": temp.high, "critical": temp.critical}
                for temp in sensors_data['coretemp']
            ]
    
    # Carga média do sistema (se disponível)
    load_avg = None
    if hasattr(psutil, "getloadavg"):
        load_avg = psutil.getloadavg()
    
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
            "iowait": getattr(cpu_times, 'iowait', None)
        },
        "cpu_times_percent": {
            "user": cpu_times_percent.user,
            "system": cpu_times_percent.system,
            "idle": cpu_times_percent.idle,
            "iowait": getattr(cpu_times_percent, 'iowait', None)
        },
        "cpu_info": cpu_info,
        "cpu_temperatures": cpu_temperatures,
        "load_avg": load_avg
    })
