#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
JM="$ROOT/1_Scripts/jmeter/plan_pruebas.jmx"
OUT_J="$ROOT/3_Ejecuciones/resultados/jmeter/resultados_$(date +%Y%m%d_%H%M%S).csv"
OUT_K="$ROOT/3_Ejecuciones/resultados/k6/summary_$(date +%Y%m%d_%H%M%S).json"

: "${JMETER_BIN:?Debe definir JMETER_BIN con la ruta a 'jmeter' (por ejemplo ~/tools/apache-jmeter-5.6.3/bin/jmeter)}"
: "${K6_BIN:=k6}"

USERS="${USERS:-10}"
RAMP="${RAMP:-10}"
LOOPS="${LOOPS:-2}"

echo "=== Ejecutando JMeter (ruta absoluta) ==="
"$JMETER_BIN" -n -t "$JM" -JUSERS="$USERS" -JRAMP="$RAMP" -JLOOPS="$LOOPS" -l "$OUT_J"

echo "=== Ejecutando k6 (si está definido/instalado) ==="
if command -v "$K6_BIN" >/dev/null 2>&1; then
  "$K6_BIN" run "$ROOT/1_Scripts/k6/smoke.js" --summary-export="$OUT_K" || true
else
  echo "k6 no encontrado; se omite humo."
fi

echo "=== Generando informe ==="
python3 "$ROOT/2_Documentacion_Tecnica/generar_informe.py" "$OUT_J" "$OUT_K" || true
echo "Listo."
