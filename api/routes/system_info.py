from flask import Blueprint, jsonify
import requests

from config.settings import get_api_url

# Cria o Blueprint para a rota /system-info
system_info_bp = Blueprint('system_info', __name__)


# Bloco 1: Endereços IPV4 e IPV6 da máquina
def get_network_info():
    
    """

    Obtém os endereços IPv4 e IPv6 da máquina.
    Retorna um dicionário com os endereços ou "N/A" se não encontrados.

    """

    network_response = requests.get(get_api_url("network"))
    network_data = network_response.json()
    ipv4_address = "N/A"
    ipv6_address = "N/A"

    # Valores esperados para as famílias de endereços (IPv4 e IPv6)
    AF_INET_VALUES = [
        "2", 
        "AF_INET", 
        "inet",  
        "IPv4",  
        "ipv4",
        "AddressFamily.AF_INET"
    ]

    AF_INET6_VALUES = [
        "10",  
        "AF_INET6", 
        "inet6", 
        "IPv6",  
        "ipv6",
        "AddressFamily.AF_INET6"  
    ]

    # Itera sobre as interfaces de rede
    for interface, data in network_data.items():

        if "addresses" in data:
            addresses = data["addresses"]

            for addr in addresses:

                family = addr["family"]

                if family in AF_INET_VALUES and ipv4_address == "N/A":
                    ipv4_address = addr["address"]
                elif family in AF_INET6_VALUES and ipv6_address == "N/A":
                    ipv6_address = addr["address"]

        if ipv4_address != "N/A" and ipv6_address != "N/A":
            break

    return {"ipv4": ipv4_address, "ipv6": ipv6_address}

# Bloco 2: Obtém o tempo de atividade (uptime)
def get_uptime():

    """
    Obtém o tempo de atividade da máquina em segundos, minutos e horas.
    Retorna um dicionário com os valores.
    """

    uptime_response = requests.get(get_api_url("uptime"))

    uptime_data = uptime_response.json()
    return {
        "seconds": uptime_data.get("uptime_seconds", 0),
        "minutes": uptime_data.get("uptime_minutes", 0),
        "hours": uptime_data.get("uptime_hours", 0)
}

# Bloco 3: Obtém o uso de memória
def get_memory_usage():

    """
    Obtém o uso de memória da máquina.
    Retorna um dicionário com a memória usada, livre, total e porcentagens.
    """

    memory_response = requests.get(get_api_url("memory"))
    memory_data = memory_response.json()
    return {
        "used_gb": round(memory_data.get("used_memory", 0) / (1024 ** 3), 2),  # Converte bytes para GB
        "free_gb": round(memory_data.get("free_memory", 0) / (1024 ** 3), 2),  # Converte bytes para GB
        "total_gb": round(memory_data.get("total_memory", 0) / (1024 ** 3), 2),  # Converte bytes para GB
        "used_percent": memory_data.get("memory_percent", 0),
        "free_percent": 100 - memory_data.get("memory_percent", 0)
    }

# Bloco 4: Obtém o uso de disco
def get_disk_usage():

    """
    Obtém o uso de disco da máquina.
    Retorna um dicionário com o espaço usado, livre, total e porcentagens.
    """

    disk_response = requests.get(get_api_url("disk"))
    disk_data = disk_response.json()
    return {
        "used_gb": disk_data.get("used_space_gb", 0),
        "free_gb": disk_data.get("free_space_gb", 0),
        "total_gb": disk_data.get("total_space_gb", 0),
        "used_percent": disk_data.get("percent_used", 0),
        "free_percent": 100 - disk_data.get("percent_used", 0)
    }

# Bloco 5: Obtém o uso de CPU por núcleo
def get_cpu_usage():

    """
    Obtém o uso da CPU por núcleo.

    Retorna uma lista com a porcentagem de uso de cada núcleo.

    """

    cpu_response = requests.get(get_api_url("cpu"))
    cpu_data = cpu_response.json()
    cpu_usage_per_core = cpu_data.get("cpu_usage_per_core", [])

    return cpu_usage_per_core

# Bloco 6: Consolida todas as informações
def consolidate_system_info():

    """
    Consolida todas as informações do sistema em um único dicionário.
    Retorna o dicionário pronto para ser convertido em JSON.
    """

    return {
        "ip_address": get_network_info(),
        "uptime": get_uptime(),
        "memory_usage": get_memory_usage(),
        "disk_usage": get_disk_usage(),
        "cpu_usage_per_core": get_cpu_usage()
    }

"""

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
    "ip_address": {
        "ipv4": "172.24.34.239",
        "ipv6": "fe80::215:5dff:feae:5070%eth0"
    },
    
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

Essa rota pode ser usada para obter todas as informações necessárias em uma única chamada, facilitando a criação de gráficos e o monitoramento do sistema. 
O usuário não precisa calcular nada, pois os dados já vêm prontos para uso.

"""

@system_info_bp.route('/', methods=['GET'])
def get_system_info():

    try:
        return jsonify(consolidate_system_info())

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Erro ao acessar os endpoints internos: {str(e)}"}), 500