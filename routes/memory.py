import psutil
from flask import Flask, Blueprint, jsonify

# Blueprint for Memory routes
memory_bp = Blueprint('memory', __name__)

"""
Endpoint: /memory
Método: GET

Descrição: Retorna informações detalhadas sobre o uso de memória RAM e memória swap, incluindo a quantidade total, usada, livre e disponível de memória, bem como a porcentagem de uso.

Exemplo de Resposta:

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

Uso esperado:

Ideal para monitorar o uso de memória no sistema e detectar quando a memória está próxima de ser completamente utilizada, o que pode afetar o desempenho.
"""

@memory_bp.route('/', methods=['GET'])
def get_memory_info():
    
    # Obtém informações de memória
    memory = psutil.virtual_memory() if hasattr(psutil, "virtual_memory") else None
    swap = psutil.swap_memory() if hasattr(psutil, "swap_memory") else None

    return jsonify({
        "total_memory": memory.total if memory else None,
        "available_memory": memory.available if memory else None,
        "used_memory": memory.used if memory else None,
        "free_memory": memory.free if memory else None,
        "memory_percent": memory.percent if memory else None,
        "swap_total": swap.total if swap else None,
        "swap_used": swap.used if swap else None,
        "swap_free": swap.free if swap else None,
        "swap_percent": swap.percent if swap else None
    })
