# OpsLinux - Monitoramento de Recursos Linux

OpsLinux é um sistema de monitoramento de recursos de um sistema Linux, desenvolvido em Python utilizando o framework Flask. Ele fornece uma API RESTful que permite monitorar diversos aspectos do sistema, como uso de CPU, memória, disco, rede, processos em execução e tempo de atividade (uptime).

![OpsLinux](https://github.com/user-attachments/assets/6d1f35ac-d8d8-4824-9139-c28f145ac2ff)

---

## 🌟 Funcionalidades

OpsLinux oferece os seguintes endpoints para monitoramento:

- **CPU**: Informações detalhadas sobre o processador, incluindo uso por núcleo, frequência, tempos de execução e temperatura.
- **Disco**: Informções sobre o espaço em disco, incluindo partições, espaço total, utilizado e livre, além de estatísticas de I/O.
- **Memória**: Monitoramento da memória RAM e swap, exibindo total, usado, livre e porcentagem de uso.
- **Rede**: Exibe dados das interfaces de rede, incluindo endereços IP, estatísticas de tráfego e status da interface.
- **Processos**: Lista de processos em execução, com detalhes como PID, nome, usuário, uso de CPU e memória, e tempo de execução.
- **Uptime**: Tempo de atividade do sistema desde o último boot.
- **System Info**: Informações consolidadas do sistema, incluindo endereço IP, tempo de atividade, uso de memória, disco e CPU.

---

## 🧐 Como Funciona

O projeto utiliza dois agentes de IA para melhorar a interação com o sistema de monitoramento:

### 🔧 Agente docBot

O **docBot** interpreta perguntas em linguagem natural e determina qual endpoint da API deve ser chamado. Ele analisa a consulta do usuário e busca as informações relevantes.

### 💻 Agente SysBot

O **SysBot** recebe os dados da API e os apresenta de forma clara e compreensível, utilizando linguagem natural. Além disso, ele gera diagramas visuais com Mermaid.js para facilitar a compreensão.

---

## 📈 Exemplo de Interação

- **Usuário**: "Qual é o uso da CPU?"
- **docBot**: Identifica a consulta e chama o endpoint correspondente.
- **SysBot**: Traduz os dados da API para algo como: "O núcleo 1 está usando 45% da capacidade, o núcleo 2 está com 30% de uso, e o núcleo 3 está com 60%." Também gera um gráfico visual do uso de cada núcleo utilizando Mermaid.js.

---

## 💪 Como Usar

### 🔧 Pré-requisitos

- Python 3.x
- Flask
- psutil

### 🛠️ Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/sistema-monitoramento.git
   cd sistema-monitoramento
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o servidor Flask:

   ```bash
   python app.py
   ```

4. Acesse a API no navegador:

   ```
   http://localhost:5002/
   ```

---

## 👨‍👩‍👦 Desenvolvedores

[![MichelleGomes](https://img.shields.io/badge/Desenvolvedor-MichelleGomes-darkblue)](https://github.com/michelleGomes85)  
[![Gabriel Barbosa](https://img.shields.io/badge/Desenvolvedor-Gabriel%20Barbosa-darkblue)](https://github.com/GabrielBarbosaAfo)

---

🌐 Projeto open-source desenvolvido para facilitar o monitoramento de sistemas Linux de forma simples e intuitiva. Contribuições são bem-vindas! 🛠️
