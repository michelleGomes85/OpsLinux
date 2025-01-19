
# Informações sobre a CPU
----------------------

**Endpoint:** `/cpu`  
**Method:** `GET`

## Descrição

Retorna informações sobre o processador do sistema, incluindo o número de núcleos, o uso da CPU por núcleo, a frequência atual, mínima e máxima da CPU, e a temperatura (caso seja suportado pelo hardware).

## Exemplo de Resposta

```json
{
    "cpu_count": 8,
    "cpu_usage_per_core": [15.0, 20.5, 10.0, 30.0, 25.5, 40.0, 18.0, 12.0],
    "cpu_frequency": {
        "current": 2600.0,
        "min": 800.0,
        "max": 3200.0
    },
    "cpu_temperatures": [
        {"label": "Core 0", "current": 45.0, "high": 70.0, "critical": 85.0},
        {"label": "Core 1", "current": 47.0, "high": 70.0, "critical": 85.0}
    ]
}
```

## Uso Esperado

Essa rota pode ser utilizada para monitorar o desempenho da CPU, identificar problemas de sobrecarga e verificar as temperaturas dos núcleos do processador.