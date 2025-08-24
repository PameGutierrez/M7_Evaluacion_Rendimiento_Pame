# Informe – Configuración, problemas y soluciones

## Configuración elegida
- Apache JMeter 5.6.3 (Java 23), ejecución Non-GUI.
- Escenarios HTTP sobre reqres.in:
  1) GET /api/users?page=2
  2) GET /api/users/2
  3) POST /api/login (JSON; credenciales desde CSV)
- Plan: 1_Scripts/jmeter/plan_pruebas.jmx con CSV Data Set Config (datasets/login.csv)
- Parámetros: USERS, RAMP (s), LOOPS

## Problemas identificados
- Política de ejecución de PowerShell (bloqueo de scripts).
- PATH incompleto (faltaba System32 y/o Java).
- JMeter no encontraba Java.
- Publicación del informe en GitHub Pages (404 y build de Jekyll).

## Soluciones aplicadas
- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass y Unblock-File.
- PATH saneado en la sesión: C:\Windows\System32; C:\apache-jmeter-5.6.3\bin; %JAVA_HOME%\bin
- Definición de JAVA_HOME (JDK 23).
- Generación del dashboard: jmeter -g <csv> -o .\docs\jmeter-dashboard
- GitHub Pages: Branch main, Folder /docs y .nojekyll para servir estáticos.

## Recomendaciones
- Escalar carga (USERS 10→50→100) y vigilar p95 < 800 ms y errores < 5%.
- Añadir Assertions y revisar keep-alive/compresión/caché.
- Considerar escalado horizontal y repetir pruebas.
