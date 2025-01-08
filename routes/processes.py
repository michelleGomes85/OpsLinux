import psutil
from flask import Flask, Blueprint, jsonify
import os
import time

# Blueprint for Processes routes
processes_bp = Blueprint('processes', __name__)

"""
PID
Usuário
Tempo de execução
Comando que originou o processo
Consumo de CPU
Consumo de memória
Exemplo de Resposta da API
json
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
]"""
@processes_bp.route('/', methods=['GET'])
def get_processes_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline']):
        try:
            process_info = proc.info
            process_info['execution_time'] = time.time() - proc.create_time()  # Calculate execution time
            process_info['cmdline'] = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""  # Command line
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Ignore processes that are no longer available or inaccessible
            pass

    # Sorting by CPU usage in descending order
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    return jsonify(processes)