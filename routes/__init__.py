"""

Módulo de Rotas da API

Este pacote contém as rotas da API RESTful, organizadas por funcionalidade. 
Cada arquivo neste diretório representa uma rota específica, responsável por expor informações do sistema Linux.

- Estrutura das Rotas:

- uptime.py: Fornece o tempo de atividade (uptime) da máquina.
- memory.py: Retorna informações sobre o uso de memória, incluindo total, usado, e livre.
- disk.py: Exibe informações detalhadas sobre o espaço em disco, como total, usado e livre.
- cpu.py: Mostra o número de núcleos da CPU e o uso percentual de cada núcleo.
- network.py: Retorna informações sobre as interfaces de rede, como endereço IP e máscara de sub-rede.
- processes.py: Lista os processos em execução com detalhes como PID, usuário, consumo de CPU e memória.

- Como Funciona:

Cada arquivo de rota utiliza o módulo `Blueprint` do Flask para criar rotas específicas, 
que são registradas no arquivo principal `app.py`. Isso permite uma organização modular, 
facilitando a manutenção e expansão da aplicação.

Exemplo de Registro de Rota no `app.py`:

```python
from flask import Flask
from routes.uptime import uptime_bp
from routes.disk import disk_bp

app = Flask(__name__)
app.register_blueprint(uptime_bp, url_prefix='/uptime')
app.register_blueprint(disk_bp, url_prefix='/disk')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

"""