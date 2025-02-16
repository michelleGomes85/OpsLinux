from flask import Blueprint, jsonify
import psutil

disk_bp = Blueprint('disk', __name__)

"""
# Disk

Endpoint: /disk
Método: GET

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
"""

@disk_bp.route('/', methods=['GET'])
def get_disk_info():
    disk = psutil.disk_usage('/')
    
    # Verifica se psutil suporta a funcionalidade
    partitions = psutil.disk_partitions() if hasattr(psutil, "disk_partitions") else []
    disk_info = []
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total_space_gb": round(usage.total / (1024**3), 2),
                "used_space_gb": round(usage.used / (1024**3), 2),
                "free_space_gb": round(usage.free / (1024**3), 2),
                "percent_used": usage.percent
            }
            disk_info.append(partition_info)
        except PermissionError:
            continue
    
    # Estatísticas de I/O do disco
    disk_io = psutil.disk_io_counters() if hasattr(psutil, "disk_io_counters") else None
    disk_io_info = {
        "read_count": disk_io.read_count if disk_io else None,
        "write_count": disk_io.write_count if disk_io else None,
        "read_bytes_gb": round(disk_io.read_bytes / (1024**3), 2) if disk_io else None,
        "write_bytes_gb": round(disk_io.write_bytes / (1024**3), 2) if disk_io else None,
        "read_time_ms": disk_io.read_time if disk_io else None,
        "write_time_ms": disk_io.write_time if disk_io else None
    }
    
    return jsonify({
        "partitions": disk_info,
        "disk_io": disk_io_info,
        "total_space_gb": round(disk.total / (1024**3), 2),
        "used_space_gb": round(disk.used / (1024**3), 2),
        "free_space_gb": round(disk.free / (1024**3), 2),
        "percent_used": disk.percent
    })
