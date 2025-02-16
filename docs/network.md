# Informações sobre a Rede
------------------------

**Endpoint:** `/network`  
**Method:** `GET`

## Descrição

Retorna informações detalhadas sobre as interfaces de rede da máquina, incluindo:

- Nome da interface.
- Endereços IP (IPv4 e IPv6) e endereço MAC.
- Máscara de sub-rede e família de endereço.
- Estatísticas de rede 
    - Bytes enviados e recebidos
    - Pacotes enviados e recebidos.
    - Erros de entrada e saída.
    - Pacotes descartados (drops) de entrada e saída.

- Status da interface
    - Se está ativa (`is_up`).
    - Modo de operação (`duplex`).
    - Velocidade da interface (`em Mbps`).
    - MTU (Maximum Transmission Unit).

Além disso, a resposta inclui o gateway padrão e a máscara de sub-rede da rede.

## Exemplo de Resposta:

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
                "netmask": "ffff:ffff:ffff:ffff::",
                "family": "AddressFamily.AF_PACKET"
            }
        ],
        "stats": {
            "bytes_sent": 1024000,
            "bytes_recv": 2048000,
            "packets_sent": 1000,
            "packets_recv": 2000,
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
            "bytes_sent": 512000,
            "bytes_recv": 512000,
            "packets_sent": 500,
            "packets_recv": 500,
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

## Uso Esperado:

- **Monitoramento de rede:** Verificar o status e o desempenho das interfaces de rede.
- **Diagnóstico de problemas:** Identificar erros, pacotes descartados ou interfaces inativas.
- **Configuração de rede:** Obter informações detalhadas sobre endereços IP, máscaras de sub-rede e gateway padrão.