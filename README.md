# Proyecto M7 · Evaluación de Rendimiento y Escalabilidad

## Requisitos previos
- **JMeter 5.6+** en PATH
- **k6** en PATH
- **Python 3.9+** con pandas, matplotlib, numpy

## Estructura
```
run_all.sh
run_all.ps1
1_Scripts/
  jmeter/plan_pruebas.jmx
  jmeter/datasets/login.csv
  k6/smoke.js
  k6/stress.js
2_Documentacion_Tecnica/
  Plan_de_Pruebas.md
  KPIs.md
  generar_informe.py
3_Ejecuciones/
  resultados/{jmeter,k6}/  # Se llenan al ejecutar
  informes/                # Informe y gráficos
4_Presentacion/
  Presentacion.md
5_Moodle/
  mosaico.md
```

## Uso 
- **Windows**: `./run_all.ps1 -USERS 10 -RAMP 10 -LOOPS 2`
- **Linux/macOS**:
  ```bash
  export USERS=10 RAMP=10 LOOPS=2
  bash ./run_all.sh
  ```

El informe final se genera en `3_Ejecuciones/informes/Informe_Resultados.md`.


## Solo JMeter (sin k6)
- **Windows (PowerShell):**
  ```powershell
  .\run_jmeter_only.ps1 -USERS 10 -RAMP 10 -LOOPS 2
  ```
- **Si PowerShell bloquea scripts:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\run_jmeter_only.ps1 -USERS 10 -RAMP 10 -LOOPS 2
  ```
- **macOS/Linux:**
  ```bash
  export USERS=10 RAMP=10 LOOPS=2
  bash ./run_jmeter_only.sh
  ```
Esto genera `Informe_Resultados_JMeter.md` con tablas y gráficas a partir de **resultados**.
