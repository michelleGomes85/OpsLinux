
# Informações sobre os Processos
----------------------------

**Endpoint:** `/processes`  
**Method:** `GET`

## Descrição

Retorna uma lista de processos em execução no sistema, com as seguintes informações:

- PID do processo
- Nome do processo
- Usuário responsável pelo processo
- Percentual de uso de CPU e memória
- Tempo de criação do processo
- Tempo de execução (em segundos)
- Comando que originou o processo

## Exemplo de Resposta

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

## Uso esperado:

Esta rota é útil para monitorar o consumo de recursos dos processos em execução no sistema. 
Ela pode ser usada para identificar processos que estão consumindo muita CPU ou memória e, assim, auxiliar na otimização do uso de recursos do sistema.