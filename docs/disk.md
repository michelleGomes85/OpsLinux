# Informações sobre o Disco
-------------------------

**Endpoint:** `/disk`  
**Method:** `GET`

## Descrição 

Retorna informações detalhadas sobre o espaço em disco do sistema, incluindo o total, espaço utilizado, espaço livre e a porcentagem de uso.

## Exemplo de Resposta

```json
{
    "total_space_gb": 500.11,
    "used_space_gb": 250.34,
    "free_space_gb": 249.77,
    "percent_used": 50.1
}
```

## Uso Esperado

Essa rota pode ser utilizada para monitorar o uso do disco, identificando quando o espaço livre está baixo, e ajudando na prevenção de problemas de armazenamento.