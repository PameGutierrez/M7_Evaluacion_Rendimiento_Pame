# Plan de Pruebas de Rendimiento

## Objetivos
- Evaluar tiempos de respuesta promedio y percentiles (p90, p95, p99).
- Medir throughput (req/s) y tasa de error.
- Identificar cuellos de botella y proponer mejoras.

## Alcance y Escenarios
1. **Flujo básico**: GET lista de usuarios → GET usuario → POST login.
2. **Lecturas repetidas**: GET lista de usuarios con diferentes niveles de concurrencia.
3. **Stress**: Escalada de usuarios con k6 (stages 10 → 30 → 50).

## Datos de prueba
- `datasets/login.csv` con emails/passwords de ejemplo soportados por reqres.in

## Configuración de carga
- Usuarios: 10, 50, 100
- Ramp-up: 10s / 30s / 30s
- Loops: 2

## Métricas a recolectar
- `avg`, `p90`, `p95`, `p99` en ms
- Throughput (req/s)
- Error rate (%)

## Criterios de aceptación (ejemplo)
- p95 < 800 ms
- Error rate < 5%
