
# Informações sobre a CPU
----------------------

**Endpoint:** `/cpu`  
**Method:** `GET`

## Descrição:

Retorna informações detalhadas sobre o processador do sistema, incluindo:

- Número de núcleos lógicos e físicos
- Uso da CPU por núcleo e total
- Frequência mínima, máxima e atual da CPU
- Tempos de execução da CPU
- Informações gerais da CPU (se disponível)
- Temperatura da CPU (se suportado pelo hardware)
- Carga média do sistema (apenas em sistemas compatíveis)

## Exemplo de Resposta:

```json
{
    "cpu_count": 8,
    "cpu_physical_count": 4,
    "cpu_usage_per_core": [15.0, 20.5, 10.0, 30.0, 25.5, 40.0, 18.0, 12.0],
    "cpu_usage_total": 25.4,
    "cpu_frequency": {
        "current": 2600.0,
        "min": 800.0,
        "max": 3200.0
    },

    "cpu_times": {
        "user": 12345.6,
        "system": 6789.0,
        "idle": 98765.4,
        "iowait": 234.5
    },

    "cpu_times_percent": {
        "user": 30.0,
        "system": 15.0,
        "idle": 50.0,
        "iowait": 5.0
    },

    "cpu_info": {
        "brand": "Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz",
        "arch": "x86_64",
        "bits": 64,
        "cores": 4,
        "threads": 8
    },

    "cpu_temperatures": [
        {"label": "Core 0", "current": 45.0, "high": 70.0, "critical": 85.0},
        {"label": "Core 1", "current": 47.0, "high": 70.0, "critical": 85.0}
    ],

    "load_avg": [1.25, 1.10, 0.95]
}
```

## Uso Esperado

Pode ser utilizado para monitorar o desempenho da CPU, identificar problemas de sobrecarga e verificar temperaturas dos núcleos do processador.