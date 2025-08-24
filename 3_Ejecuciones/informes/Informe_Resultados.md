# Informe de Resultados

## Resumen ejecutivo
Se realizaron ejecuciones sintéticas para ilustrar el análisis con 10, 50 y 100 usuarios concurrentes. Se incluyen gráficos de tiempos y throughput.

## Hallazgos
- El p95 se mantiene bajo 800 ms para 10 y 50 usuarios; a 100 usuarios se acerca al umbral.
- La tasa de error promedio se mantiene por debajo del 5% en todos los escenarios.
- El throughput crece con la concurrencia, con señales de saturación a partir de 100 usuarios.

## Recomendaciones
- Optimizar endpoints críticos usados en el flujo (cache de lecturas GET).
- Revisar conexiones HTTP keep-alive y pool de threads del backend.
- Probar con infraestructura escalada horizontalmente para validar elasticidad.

## Gráficos
- `graficos/tiempos_promedio.png`
- `graficos/throughput.png`
- `graficos/percentiles.png`
