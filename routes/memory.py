import psutil
from flask import Flask, Blueprint, jsonify

# Blueprint for Memory routes
memory_bp = Blueprint('memory', __name__)

"""
Endpoint: /memory
Método: GET
Descrição: Retorna informações detalhadas sobre o uso de memória RAM e memória de swap.
Resposta
json
{
    "total_memory": 16777216000,
    "available_memory": 9876543210,
    "used_memory": 5432109876,
    "free_memory": 4444400000,
    "memory_percent": 32.4,
    "swap_total": 2147483648,
    "swap_used": 1073741824,
    "swap_free": 1073741824,
    "swap_percent": 50.0
}
"""
@memory_bp.route('/', methods=['GET'])
def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return jsonify({
        "total_memory": memory.total,
        "available_memory": memory.available,
        "used_memory": memory.used,
        "free_memory": memory.free,
        "memory_percent": memory.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percent": swap.percent
    })