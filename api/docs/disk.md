# Informações sobre o Disco
-------------------------

**Endpoint:** `/disk`  
**Method:** `GET`

## Descrição

Retorna informações detalhadas sobre o espaço em disco do sistema, incluindo:

- Espaço total
- Espaço utilizado
- Espaço livre
- Porcentagem de uso
- Informações de partições
- Estatísticas de I/O do disco

## Exemplo de Resposta
```json
{
    "partitions": [
        {
            "device": "/dev/sda1",
            "mountpoint": "/",
            "fstype": "ext4",
            "total_space_gb": 500.11,
            "used_space_gb": 250.34,
            "free_space_gb": 249.77,
            "percent_used": 50.1
        }
    ],
    "disk_io": {
        "read_count": 123456,
        "write_count": 789012,
        "read_bytes_gb": 320.45,
        "write_bytes_gb": 214.32,
        "read_time_ms": 1200,
        "write_time_ms": 800
    },
    "total_space_gb": 500.11,
    "used_space_gb": 250.34,
    "free_space_gb": 249.77,
    "percent_used": 50.1
}
```

## Uso Esperado

Essa rota pode ser utilizada para monitorar o uso do disco, identificando quando o espaço livre está baixo e ajudando na prevenção de problemas de armazenamento.
