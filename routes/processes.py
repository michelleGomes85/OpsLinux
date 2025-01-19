import psutil
from flask import Flask, Blueprint, jsonify
import time

processes_bp = Blueprint('processes', __name__)

"""

Endpoint: /processes
Método: GET

Descrição: Retorna uma lista de processos em execução no sistema, incluindo o PID, nome do processo, usuário, consumo de CPU e memória, tempo de execução e o comando que originou o processo.

```json

[
    {
        "pid": 1234,
        "name": "python",
        "username": "user1",
        "cpu_percent": 25.0,
        "memory_percent": 1.2,
        "create_time": 1673012345.67,
        "execution_time": 3600.5,
        "cmdline": "python app.py"
    },
    {
        "pid": 5678,
        "name": "chrome",
        "username": "user1",
        "cpu_percent": 15.5,
        "memory_percent": 3.4,
        "create_time": 1673005678.12,
        "execution_time": 7200.3,
        "cmdline": "/usr/bin/google-chrome-stable --no-sandbox"
    }
]
```

Uso esperado:

A rota é útil para monitorar o consumo de recursos dos processos em execução no sistema e identificar processos que consomem muita CPU ou memória.
"""
@processes_bp.route('/', methods=['GET'])
def get_processes_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline']):
        try:
            process_info = proc.info
            process_info['execution_time'] = time.time() - proc.create_time()  
            process_info['cmdline'] = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""  
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    return jsonify(processes)