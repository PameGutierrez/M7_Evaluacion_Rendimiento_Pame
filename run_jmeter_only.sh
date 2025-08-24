#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
JM="$ROOT/1_Scripts/jmeter/plan_pruebas.jmx"
timestamp="$(date +%Y%m%d_%H%M%S)"
OUT_J="$ROOT/3_Ejecuciones/resultados/jmeter/resultados_${timestamp}.csv"

USERS="${USERS:-10}"
RAMP="${RAMP:-10}"
LOOPS="${LOOPS:-2}"

echo "=== Ejecutando JMeter (Non-GUI) ==="
jmeter -n -t "$JM" -JUSERS="$USERS" -JRAMP="$RAMP" -JLOOPS="$LOOPS" -l "$OUT_J"

echo "=== Generando informe (solo JMeter) ==="
python3 "$ROOT/2_Documentacion_Tecnica/generar_informe_jmeter_solo.py" "$OUT_J"

echo "Listo. Revisa 3_Ejecuciones/informes/Informe_Resultados_JMeter.md"
