from flask import Blueprint, jsonify
import requests

system_info_bp = Blueprint('system_info', __name__)

"""

Aqui está a documentação para a rota /system-info:

Endpoint: /system-info
Método: GET

Descrição: Retorna um JSON consolidado com as informações do sistema, incluindo:
- Endereço IP (obtido do endpoint /network)
- Tempo de atividade da máquina (obtido do endpoint /uptime)
- Uso de memória: porcentagem usada, parte usada e parte livre (obtido do endpoint /memory)
- Uso de disco: porcentagem usada, parte usada e parte livre (obtido do endpoint /disk)
- Porcentagem de consumo de CPU por núcleo (obtido do endpoint /cpu)

Exemplo de Resposta:

'''json
{
    "ip_address": "192.168.0.10",
    "uptime": {
        "seconds": 123456.78,
        "minutes": 2057.61,
        "hours": 34.29
    },
    "memory_usage": {
        "used_gb": 5.43,
        "free_gb": 11.33,
        "total_gb": 16.76,
        "used_percent": 32.4,
        "free_percent": 67.6
    },
    "disk_usage": {
        "used_gb": 250.34,
        "free_gb": 249.77,
        "total_gb": 500.11,
        "used_percent": 50.1,
        "free_percent": 49.9
    },
    "cpu_usage_per_core": [15.0, 20.5, 10.0, 30.0, 25.5, 40.0, 18.0, 12.0]
}
'''

Uso Esperado:

Essa rota pode ser usada para obter todas as informações necessárias em uma única chamada, facilitando a criação de gráficos e o monitoramento do sistema. O usuário não precisa calcular nada, pois os dados já vêm prontos para uso.

"""

@system_info_bp.route('/', methods=['GET'])
def get_system_info():
    
    # URL base da API (ajuste conforme necessário)
    API_BASE_URL = "http://localhost:5000"

    try:
        # Obtém o endereço IP do endpoint /network
        network_response = requests.get(f"{API_BASE_URL}/network")
        network_data = network_response.json()
        ip_address = network_data.get("eth0", [{}])[0].get("address", "N/A")

        # Obtém o tempo de atividade do endpoint /uptime
        uptime_response = requests.get(f"{API_BASE_URL}/uptime")
        uptime_data = uptime_response.json()

        # Obtém o uso de memória do endpoint /memory
        memory_response = requests.get(f"{API_BASE_URL}/memory")
        memory_data = memory_response.json()
        memory_usage = {
            "used_gb": round(memory_data.get("used_memory", 0) / (1024 ** 3), 2),  # Convertendo bytes para GB
            "free_gb": round(memory_data.get("free_memory", 0) / (1024 ** 3), 2),  # Convertendo bytes para GB
            "total_gb": round(memory_data.get("total_memory", 0) / (1024 ** 3), 2),  # Convertendo bytes para GB
            "used_percent": memory_data.get("memory_percent", 0),
            "free_percent": 100 - memory_data.get("memory_percent", 0)
        }

        # Obtém o uso de disco do endpoint /disk
        disk_response = requests.get(f"{API_BASE_URL}/disk")
        disk_data = disk_response.json()
        disk_usage = {
            "used_gb": disk_data.get("used_space_gb", 0),
            "free_gb": disk_data.get("free_space_gb", 0),
            "total_gb": disk_data.get("total_space_gb", 0),
            "used_percent": disk_data.get("percent_used", 0),
            "free_percent": 100 - disk_data.get("percent_used", 0)
        }

        # Obtém o uso de CPU por núcleo do endpoint /cpu
        cpu_response = requests.get(f"{API_BASE_URL}/cpu")
        cpu_data = cpu_response.json()
        cpu_usage_per_core = cpu_data.get("cpu_usage_per_core", [])

        # Consolida os dados
        system_info = {
            "ip_address": ip_address,
            "uptime": {
                "seconds": uptime_data.get("uptime_seconds", 0),
                "minutes": uptime_data.get("uptime_minutes", 0),
                "hours": uptime_data.get("uptime_hours", 0)
            },
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "cpu_usage_per_core": cpu_usage_per_core
        }

        return jsonify(system_info)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao acessar os endpoints internos: {str(e)}"}), 500