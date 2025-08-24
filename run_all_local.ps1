Param(
  [Parameter(Mandatory=$true)][string]$JMeterPath,
  [string]$K6Path = "k6",
  [int]$USERS = 10,
  [int]$RAMP = 10,
  [int]$LOOPS = 2
)
$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$JM = Join-Path $ROOT "1_Scripts/jmeter/plan_pruebas.jmx"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$OUT_J = Join-Path $ROOT "3_Ejecuciones/resultados/jmeter/resultados_$timestamp.csv"
$OUT_K = Join-Path $ROOT "3_Ejecuciones/resultados/k6/summary_$timestamp.json"

Write-Host "=== Ejecutando JMeter (ruta absoluta) ==="
& $JMeterPath -n -t $JM -JUSERS=$USERS -JRAMP=$RAMP -JLOOPS=$LOOPS -l $OUT_J

Write-Host "=== Ejecutando k6 (si está presente) ==="
try {
  & $K6Path run (Join-Path $ROOT "1_Scripts/k6/smoke.js") --summary-export="$OUT_K"
} catch {
  Write-Warning "k6 no encontrado o falló la ejecución; se omite humo."
}

Write-Host "=== Generando informe ==="
try {
  python (Join-Path $ROOT "2_Documentacion_Tecnica/generar_informe.py") $OUT_J $OUT_K
} catch {
  Write-Warning "No se pudo generar el informe automáticamente."
}
Write-Host "Listo."
