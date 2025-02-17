# OpsLinux

Este projeto é um sistema de monitoramento de recursos de um sistema Linux, desenvolvido em Python utilizando o framework Flask. Ele fornece uma API RESTful que permite monitorar diversos aspectos do sistema, como uso de CPU, memória, disco, rede, processos em execução e tempo de atividade (uptime).

## Funcionalidades

O sistema oferece os seguintes endpoints:

- **CPU**: Informações detalhadas sobre o processador, incluindo uso por núcleo, frequência, tempos de execução e temperatura.
- **Disco**: Informações sobre o espaço em disco, incluindo partições, espaço total, utilizado e livre, além de estatísticas de I/O.
- **Memória**: Informações sobre o uso de memória RAM e swap, incluindo total, usado, livre e porcentagem de uso.
- **Rede**: Informações sobre as interfaces de rede, incluindo endereços IP, estatísticas de tráfego e status da interface.
- **Processos**: Lista de processos em execução, com detalhes como PID, nome, usuário, uso de CPU e memória, e tempo de execução.
- **Uptime**: Tempo de atividade do sistema, incluindo segundos, minutos, horas e dias desde o último boot.
- **System Info**: Informações consolidadas do sistema, incluindo endereço IP, tempo de atividade, uso de memória, disco e CPU.

![image](https://github.com/user-attachments/assets/6d1f35ac-d8d8-4824-9139-c28f145ac2ff)

![image](https://github.com/user-attachments/assets/b4457766-cb2c-46b1-aa5c-174f87282c2c)

## Como Usar

### Pré-requisitos

- Python 3.x
- Flask
- psutil

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/sistema-monitoramento.git
   cd sistema-monitoramento


### Instale as dependências:
    pip install -r requirements.txt

### Execute o servidor Flask:
    python app.py

### Acesse a API no navegador
    http://localhost:5002/
