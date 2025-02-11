# Informações sobre o Disco
-------------------------

**Endpoint:** `/disk`  
**Method:** `GET`

## Descrição 

Retorna informações detalhadas sobre o espaço em disco do sistema, incluindo o total, espaço utilizado, espaço livre e a porcentagem de uso.

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
        },
        {
            "device": "/dev/sdb1",
            "mountpoint": "/mnt/data",
            "fstype": "ntfs",
            "total_space_gb": 1000.0,
            "used_space_gb": 500.0,
            "free_space_gb": 500.0,
            "percent_used": 50.0
        }
    ],
    "disk_io": {
        "read_count": 123456,
        "write_count": 654321,
        "read_bytes_gb": 12.34,
        "write_bytes_gb": 65.43,
        "read_time_ms": 1234,
        "write_time_ms": 5678
    }
}
```

## Uso Esperado

Essa rota pode ser utilizada para monitorar o uso do disco, identificando quando o espaço livre está baixo, e ajudando na prevenção de problemas de armazenamento.