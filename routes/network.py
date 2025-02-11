from flask import Blueprint, jsonify
import psutil
import subprocess

network_bp = Blueprint('network', __name__)

"""

Aqui está a documentação para a rota /network:

Endpoint: /network
Método: GET

Descrição: Retorna informações detalhadas sobre as interfaces de rede da máquina, incluindo nome da interface, 
endereço IP, máscara de sub-rede e família de endereço.

Exemplo de Resposta:

'''json
{
    "eth0": [
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
    "lo": [
        {
            "address": "127.0.0.1",
            "netmask": "255.0.0.0",
            "family": "AddressFamily.AF_INET"
        }
    ]
}
'''

Uso Esperado:

Essa rota pode ser usada para monitorar a configuração de rede da máquina, identificar problemas de conectividade e 
obter informações sobre os adaptadores de rede disponíveis.

"""

def get_default_gateway_and_netmask():
    """
    Obtém o gateway padrão e a máscara de sub-rede no Linux.
    Retorna um dicionário com o gateway e a máscara, ou "N/A" se não encontrado.
    """
    try:
        # Executa o comando 'ip route' para obter as rotas
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if 'default' in line:
                parts = line.split()
                gateway = parts[2]  # O gateway é o terceiro campo
                netmask = parts[7] if len(parts) > 7 else "N/A"  # A máscara é o oitavo campo (se existir)
                return {"gateway": gateway, "netmask": netmask}
    except Exception as e:
        print(f"Erro ao obter o gateway e a máscara de sub-rede: {e}")
        return {"gateway": "N/A", "netmask": "N/A"}

    return {"gateway": "N/A", "netmask": "N/A"}

@network_bp.route('/', methods=['GET'])
def get_network_info():
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
                'speed': stats.speed,  # Velocidade em Mbps
                'mtu': stats.mtu
            }

    # Adiciona o gateway padrão e a máscara de sub-rede à resposta
    gateway_info = get_default_gateway_and_netmask()
    result['default_gateway'] = gateway_info['gateway']
    result['default_netmask'] = gateway_info['netmask']

    return jsonify(result)