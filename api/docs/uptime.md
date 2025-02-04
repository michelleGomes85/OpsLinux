# Tempo de Atividade do Sistema
----------------------------

**Endpoint:** `/api/uptime`  
**Method:** `GET`

## Descrição

Retorna o tempo de atividade do sistema em segundos, minutos e horas.

## Exemplo de Resposta

```json
{
    "uptime_seconds": 123456.78,
    "uptime_minutes": 2057.61,
    "uptime_hours": 34.29
}
```

## Uso Esperado

Essa rota pode ser usada para obter o tempo de atividade de uma máquina Linux e exibir essa informação ao usuário.