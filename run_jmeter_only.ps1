Param(
  [int]$USERS = 10,
  [int]$RAMP = 10,
  [int]$LOOPS = 2
)
$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$JM = Join-Path $ROOT "1_Scripts/jmeter/plan_pruebas.jmx"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$OUT_J = Join-Path $ROOT "3_Ejecuciones/resultados/jmeter/resultados_$timestamp.csv"

Write-Host "=== Ejecutando JMeter (Non-GUI) ==="
jmeter -n -t $JM -JUSERS=$USERS -JRAMP=$RAMP -JLOOPS=$LOOPS -l $OUT_J

Write-Host "=== Generando informe (solo JMeter) ==="
python (Join-Path $ROOT "2_Documentacion_Tecnica/generar_informe_jmeter_solo.py") $OUT_J

Write-Host "Listo. Revisa 3_Ejecuciones\informes\Informe_Resultados_JMeter.md"
