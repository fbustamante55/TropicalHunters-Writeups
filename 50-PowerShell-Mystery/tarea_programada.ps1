# ============================================================
#  Proyecto Aurora - Tarea programada: reporte semanal
#  Equipo: Administracion de sistemas (nodo AUR-SRV-02)
#  Ultima revision: 2026-03-14
# ============================================================
# Este script arma el encabezado del reporte semanal y lo
# muestra por pantalla. No modifica archivos ni el registro.

# --- Parametros generales del reporte ---
$tituloReporte = "Reporte semanal de operaciones - Proyecto Aurora"
$rutaDatos     = "C:\Aurora\datos\semana_actual"
$rutaSalida    = "C:\Aurora\reportes"
$nodo          = "AUR-SRV-02"
$responsable   = "admin.aurora"
$fechaReporte  = (Get-Date).ToString("yyyy-MM-dd")

# --- Valores de configuracion de la tarea ---
$sello    = "1cm9yYTogbGEgY2xhd"
$marca    = "mUgZGVsIHJlcG9ydGUgZXMgVE"
$etiqueta = "c19yZXZlbGFuX2xhX3ZlcmRhZF85OX0="
$registro = "Tm90YSBpbnRlcm5hIGRlIEF"
$codigo   = "h7dmFyaWFibGVzX3VuaWRh"

# --- Encabezado ---
Write-Output "=============================================="
Write-Output $tituloReporte
Write-Output ("Fecha de generacion : " + $fechaReporte)
Write-Output ("Nodo                : " + $nodo)
Write-Output ("Responsable         : " + $responsable)
Write-Output ("Origen de datos     : " + $rutaDatos)
Write-Output ("Carpeta de salida   : " + $rutaSalida)
Write-Output "=============================================="

# --- Nota interna (se reconstruye en tiempo de ejecucion) ---
$notaCodificada = -join ($registro, $sello, $marca, $codigo, $etiqueta)
$notaInterna = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($notaCodificada))

Write-Output ""
Write-Output ("Nota interna        : " + $notaInterna)
Write-Output "Tarea finalizada sin errores."
