# Tempo de Atividade do Sistema
----------------------------

**Endpoint:** `/uptime`  
**Method:** `GET`

## Descrição

Retorna o tempo de atividade do sistema Linux em segundos, minutos, horas e dias. 
Utiliza o arquivo `/proc/uptime` para obter o tempo de atividade do sistema desde o último boot. 
Além disso, fornece a data e hora de inicialização do sistema e uma indicação se o sistema foi recentemente reiniciado (menos de 1 minuto).

## Exemplo de Resposta

```json
{
    "uptime_seconds": 123456.78,
    "uptime_minutes": 2057.61,
    "uptime_hours": 34.29,
    "uptime_days": 1.43,
    "uptime_formatted": "1 day, 10:17:36",
    "boot_time": "2025-02-15 10:30:00",
    "recently_rebooted": false
}
```

## Uso Esperado:

Essa rota pode ser usada para monitorar o tempo de atividade do sistema Linux. 
É útil para obter informações sobre a durabilidade do sistema em execução e saber quando ele foi reiniciado pela última vez.