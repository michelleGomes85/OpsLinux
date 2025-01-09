# Informações sobre a Memória
---------------------------

**Endpoint:** `/memory`  
**Method:** `GET`

## Descrição

Retorna informações detalhadas sobre o uso de memória RAM e memória swap, incluindo a quantidade total, usada, livre e disponível de memória, bem como a porcentagem de uso.

## Exemplo de Resposta

```json
{
    "total_memory": 16777216000,
    "available_memory": 9876543210,
    "used_memory": 5432109876,
    "free_memory": 4444400000,
    "memory_percent": 32.4,
    "swap_total": 2147483648,
    "swap_used": 1073741824,
    "swap_free": 1073741824,
    "swap_percent": 50.0
}
```

## Uso esperado

Ideal para monitorar o uso de memória no sistema e detectar quando a memória está próxima de ser completamente utilizada, o que pode afetar o desempenho.