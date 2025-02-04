# Informações sobre a Rede
------------------------

**Endpoint:** `/api/network`  
**Method:** `GET`

## Descrição

Retorna informações detalhadas sobre as interfaces de rede da máquina, incluindo nome da interface, 
endereço IP, máscara de sub-rede e família de endereço.

## Exemplo de Resposta:

```json
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
```

## Uso Esperado:

Essa rota pode ser usada para monitorar a configuração de rede da máquina, identificar problemas de conectividade e 
obter informações sobre os adaptadores de rede disponíveis.