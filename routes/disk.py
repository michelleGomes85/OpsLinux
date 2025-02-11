from flask import Blueprint, jsonify
import psutil

disk_bp = Blueprint('disk', __name__)

"""

Aqui está a documentação para a rota /disk:

Endpoint: /disk
Método: GET

Descrição: Retorna informações detalhadas sobre o espaço em disco do sistema, incluindo o total, espaço utilizado, espaço livre e a porcentagem de uso.

Exemplo de Resposta:

'''json
{
    "total_space_gb": 500.11,
    "used_space_gb": 250.34,
    "free_space_gb": 249.77,
    "percent_used": 50.1
}
'''

Uso Esperado:

Essa rota pode ser utilizada para monitorar o uso do disco, identificando quando o espaço livre está baixo, e ajudando na prevenção de problemas de armazenamento.

"""

@disk_bp.route('/', methods=['GET'])
def get_disk_info():
    disk = psutil.disk_usage('/')
    # Informações sobre todas as partições
    partitions = psutil.disk_partitions()
    disk_info = []

    for partition in partitions:
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

    # Estatísticas de I/O do disco
    disk_io = psutil.disk_io_counters()
    disk_io_info = {
        "read_count": disk_io.read_count,
        "write_count": disk_io.write_count,
        "read_bytes_gb": round(disk_io.read_bytes / (1024**3), 2),
        "write_bytes_gb": round(disk_io.write_bytes / (1024**3), 2),
        "read_time_ms": disk_io.read_time,
        "write_time_ms": disk_io.write_time
    }

    return jsonify({
        "partitions": disk_info,
        "disk_io": disk_io_info,
        'total_space_gb': round(disk.total / (1024**3), 2),
        'used_space_gb': round(disk.used / (1024**3), 2),
        'free_space_gb': round(disk.free / (1024**3), 2),
        'percent_used': disk.percent
    })
