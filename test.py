# import requests

# BASE_URL = 'http://127.0.0.1:5000'

# def test_uptime():
#     print("Testando /uptime")
#     response = requests.get(f'{BASE_URL}/uptime')
#     if response.status_code == 200:
#         uptime_data = response.json()
#         print(f"Uptime em segundos: {uptime_data['uptime_seconds']}")
#         print(f"Uptime em horas: {uptime_data['uptime_hours']:.2f}")
#     else:
#         print(f"Erro: {response.status_code}")

# if __name__ == '__main__':
#     test_uptime()

# import requests

# BASE_URL = 'http://127.0.0.1:6000'

# def test_cpu():
#     print("Testando /cpu")
#     response = requests.get(f'{BASE_URL}/cpu')
#     if response.status_code == 200:
#         cpu_data = response.json()
#         print(f"Número de núcleos: {cpu_data['cpu_count']}")
#         print(f"Uso por núcleo: {cpu_data['cpu_usage_per_core']}")
#         print("Frequência da CPU:")
#         print(f"  Atual: {cpu_data['cpu_frequency']['current']} MHz")
#         print(f"  Mínima: {cpu_data['cpu_frequency']['min']} MHz")
#         print(f"  Máxima: {cpu_data['cpu_frequency']['max']} MHz")
        
#         print("\nTemperaturas da CPU:")
#         for temp in cpu_data["cpu_temperatures"]:
#             print(f"  Núcleo: {temp['label'] or 'Desconhecido'}")
#             print(f"    Atual: {temp['current']} °C")
#             print(f"    Alta: {temp['high']} °C")
#             print(f"    Crítica: {temp['critical']} °C\n\n")
#     else:
#         print(f"Erro: {response.status_code}")

# if __name__ == '__main__':
#     test_cpu()

# import requests

# BASE_URL = 'http://127.0.0.1:6000'

# def test_memory():
#     print("Testando /memory")
#     response = requests.get(f'{BASE_URL}/memory')
#     if response.status_code == 200:
#         memory_data = response.json()
#         print("Memória RAM:")
#         print(f"  Total: {memory_data['total_memory'] / (1024**3):.2f} GB")
#         print(f"  Disponível: {memory_data['available_memory'] / (1024**3):.2f} GB")
#         print(f"  Usada: {memory_data['used_memory'] / (1024**3):.2f} GB")
#         print(f"  Livre: {memory_data['free_memory'] / (1024**3):.2f} GB")
#         print(f"  Percentual Usado: {memory_data['memory_percent']}%")
        
#         print("\nMemória de Swap:")
#         print(f"  Total: {memory_data['swap_total'] / (1024**3):.2f} GB")
#         print(f"  Usada: {memory_data['swap_used'] / (1024**3):.2f} GB")
#         print(f"  Livre: {memory_data['swap_free'] / (1024**3):.2f} GB")
#         print(f"  Percentual Usado: {memory_data['swap_percent']}%")
#     else:
#         print(f"Erro: {response.status_code}")

# if __name__ == '__main__':
#     test_memory()

import requests
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:6000'

def test_processes():
    print("Testando /processes")
    response = requests.get(f'{BASE_URL}/processes')
    if response.status_code == 200:
        processes = response.json()
        print(f"Total de processos retornados: {len(processes)}")
        print("\nTop 5 Processos por Uso de CPU:")
        print("-" * 80)
        for proc in processes[:5]:  # Exibir os 5 primeiros processos
            create_time = datetime.fromtimestamp(proc['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            execution_time = str(timedelta(seconds=int(proc['execution_time'])))
            print(f"PID: {proc['pid']}, Nome: {proc['name']}, Usuário: {proc['username']}")
            print(f"  CPU%: {proc['cpu_percent']}, Memória%: {proc['memory_percent']}")
            print(f"  Criado em: {create_time}, Tempo de execução: {execution_time}")
            print(f"  Comando: {proc['cmdline']}")
            print("-" * 80)
    else:
        print(f"Erro: {response.status_code}")

if __name__ == '__main__':
    test_processes()
