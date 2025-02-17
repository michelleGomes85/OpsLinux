from flask import Blueprint, jsonify
import psutil
import subprocess

# Cria um Blueprint para as rotas relacionadas à rede
network_bp = Blueprint('network', __name__)

def get_default_gateway_and_netmask():

    """
    Obtém o gateway padrão e a máscara de sub-rede no Linux.

    Retorna:
        dict: Um dicionário contendo o gateway padrão e a máscara de sub-rede.
              Exemplo: {"gateway": "192.168.1.1", "netmask": "255.255.255.0"}
              Se não for possível obter as informações, retorna "N/A" para ambos.
    """

    try:
        # Executa o comando 'ip route' para obter as rotas
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.splitlines():

            if 'default' in line:
                parts = line.split()

                 # O gateway é o terceiro campo
                gateway = parts[2] 

                # A máscara é o oitavo campo (se existir)
                netmask = parts[7] if len(parts) > 7 else "N/A"  
                return {"gateway": gateway, "netmask": netmask}
            
    except Exception as e:
        return {"gateway": "N/A", "netmask": "N/A"}

    return {"gateway": "N/A", "netmask": "N/A"}

@network_bp.route('/', methods=['GET'])
def get_network_info():

    """
    Endpoint: /network
    Método: GET

    Descrição:
        Retorna informações detalhadas sobre as interfaces de rede da máquina, incluindo:
        - Nome da interface
        - Endereço IP
        - Máscara de sub-rede
        - Família de endereço
        - Estatísticas de rede (bytes enviados/recebidos, pacotes, erros, etc.)
        - Status da interface (up/down, duplex, velocidade, MTU)
        - Gateway padrão e máscara de sub-rede

    Exemplo de Resposta:
        ```json
        {
            "eth0": {
                "addresses": [
                    {
                        "address": "192.168.0.10",
                        "netmask": "255.255.255.0",
                        "family": "AddressFamily.AF_INET"
                    },
                    {
                        "address": "00:1A:2B:3C:4D:5E",
                        "netmask": null,
                        "family": "AddressFamily.AF_PACKET"
                    }
                ],
                "stats": {
                    "bytes_sent": 123456,
                    "bytes_recv": 654321,
                    "packets_sent": 100,
                    "packets_recv": 200,
                    "errors_in": 0,
                    "errors_out": 0,
                    "drops_in": 0,
                    "drops_out": 0
                },
                "status": {
                    "is_up": true,
                    "duplex": 2,
                    "speed": 1000,
                    "mtu": 1500
                }
            },
            "lo": {
                "addresses": [
                    {
                        "address": "127.0.0.1",
                        "netmask": "255.0.0.0",
                        "family": "AddressFamily.AF_INET"
                    }
                ],
                "stats": {
                    "bytes_sent": 0,
                    "bytes_recv": 0,
                    "packets_sent": 0,
                    "packets_recv": 0,
                    "errors_in": 0,
                    "errors_out": 0,
                    "drops_in": 0,
                    "drops_out": 0
                },
                "status": {
                    "is_up": true,
                    "duplex": 0,
                    "speed": 0,
                    "mtu": 65536
                }
            },
            "default_gateway": "192.168.1.1",
            "default_netmask": "255.255.255.0"
        }
        ```

    Uso Esperado:

        Essa rota pode ser usada para monitorar a configuração de rede da máquina, identificar problemas de conectividade e
        obter informações sobre os adaptadores de rede disponíveis.
    """

    # Informações de endereços das interfaces
    interfaces = psutil.net_if_addrs()
    result = {}
    for interface, addresses in interfaces.items():
        result[interface] = {
            'addresses': [
                {
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'family': str(addr.family)
                } for addr in addresses
            ]
        }

    # Informações de estatísticas de rede
    io_counters = psutil.net_io_counters(pernic=True)
    for interface, stats in io_counters.items():
        if interface in result:
            result[interface]['stats'] = {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'packets_sent': stats.packets_sent,
                'packets_recv': stats.packets_recv,
                'errors_in': stats.errin,
                'errors_out': stats.errout,
                'drops_in': stats.dropin,
                'drops_out': stats.dropout
            }

    # Informações de status da interface
    if_stats = psutil.net_if_stats()
    for interface, stats in if_stats.items():
        if interface in result:
            result[interface]['status'] = {
                'is_up': stats.isup,
                'duplex': stats.duplex,
                'speed': stats.speed, 
                'mtu': stats.mtu
            }

    # Adiciona o gateway padrão e a máscara de sub-rede à resposta
    gateway_info = get_default_gateway_and_netmask()
    result['default_gateway'] = gateway_info['gateway']
    result['default_netmask'] = gateway_info['netmask']

    return jsonify(result)