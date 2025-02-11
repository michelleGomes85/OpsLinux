# Tempo de Atividade do Sistema
----------------------------

**Endpoint:** `/uptime`  
**Method:** `GET`

## Descrição

Retorna o tempo de atividade do sistema em segundos, minutos, horas e dias, além de uma representação formatada e a data/hora de inicialização.

## Exemplo de Resposta

```json
{
    "uptime_seconds": 123456.78,
    "uptime_minutes": 2057.61,
    "uptime_hours": 34.29,
    "uptime_days": 1.43,
    "uptime_formatted": "1 day, 10:17:36",
    "boot_time": "2023-10-01 12:34:56",
    "recently_rebooted": false
}
```

## Uso Esperado:
- Adicione tratamento de erros para garantir que a API funcione corretamente em sistemas onde o arquivo `/proc/uptime` não está disponível.
- Se necessário, você pode adicionar mais detalhes, como o tempo de atividade máximo já registrado ou comparações com tempos de atividade anteriores.

Essas melhorias tornarão a rota `/uptime` mais informativa e útil para monitoramento e diagnóstico do sistema.