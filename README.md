# OpsLinux

Este projeto é um sistema de monitoramento de recursos de um sistema Linux, desenvolvido em Python utilizando o framework Flask. Ele fornece uma API RESTful que permite monitorar diversos aspectos do sistema, como uso de CPU, memória, disco, rede, processos em execução e tempo de atividade (uptime).

![image](https://github.com/user-attachments/assets/6d1f35ac-d8d8-4824-9139-c28f145ac2ff)

![image](https://github.com/user-attachments/assets/b4457766-cb2c-46b1-aa5c-174f87282c2c)

## Funcionalidades

O sistema oferece os seguintes endpoints:

- **CPU**: Informações detalhadas sobre o processador, incluindo uso por núcleo, frequência, tempos de execução e temperatura.
- **Disco**: Informações sobre o espaço em disco, incluindo partições, espaço total, utilizado e livre, além de estatísticas de I/O.
- **Memória**: Informações sobre o uso de memória RAM e swap, incluindo total, usado, livre e porcentagem de uso.
- **Rede**: Informações sobre as interfaces de rede, incluindo endereços IP, estatísticas de tráfego e status da interface.
- **Processos**: Lista de processos em execução, com detalhes como PID, nome, usuário, uso de CPU e memória, e tempo de execução.
- **Uptime**: Tempo de atividade do sistema, incluindo segundos, minutos, horas e dias desde o último boot.
- **System Info**: Informações consolidadas do sistema, incluindo endereço IP, tempo de atividade, uso de memória, disco e CPU.

## Como Funciona

Este projeto usa dois agentes de IA para fornecer uma interação mais natural com o sistema de monitoramento:

### 1. Agente docBot
O **docBot** é responsável por interpretar as perguntas do usuário em linguagem natural e determinar qual endpoint da API deve ser chamado. Ele analisa a consulta do usuário e escolhe as informações relevantes do sistema com base na documentação e na solicitação.

### 2. Agente SysBot
O **SysBot** pega os dados retornados pela API e os apresenta ao usuário de forma clara e compreensível. Ele responde em linguagem natural e também usa o Mermaid.js para gerar diagramas visuais baseados nas informações do sistema, como gráficos de uso de CPU ou memória, tornando as respostas mais intuitivas e fáceis de entender.

## Exemplo de Interação
- **Usuário**: "Qual é o uso da CPU?"
- **docBot**: Detecta que a consulta é sobre o uso de CPU e chama o endpoint correspondente.
- **SysBot**: Recebe os dados da API, traduz para uma resposta em linguagem natural, como: "O núcleo 1 está usando 45% da capacidade, o núcleo 2 está com 30% de uso, e o núcleo 3 está com 60%." E gera um gráfico visual do uso de cada núcleo utilizando Mermaid.js.

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
