# =====================================================
#  NovaTech Labs - Mantenimiento semanal de estaciones
#  Autor: Soporte TI (turno nocturno)
#  Uso: revisar rutas de registro y mostrar un resumen
# =====================================================

$empresa        = "NovaTech Labs"
$estacion       = "NT-LAB-07"
$carpetaLogs    = "C:\NovaTech\Logs"
$carpetaTemp    = "C:\NovaTech\Temp"
$archivoResumen = "$carpetaLogs\resumen_semanal.txt"
$diasRetencion  = 30
$subcarpetas    = @("sistema", "aplicaciones", "respaldos")

Write-Output "Mantenimiento de $empresa - estacion $estacion"
Write-Output "Carpeta de registros: $carpetaLogs"
Write-Output "Carpeta temporal: $carpetaTemp"
Write-Output "Retencion de registros: $diasRetencion dias"

# Listar las subcarpetas de registro que se revisan cada semana
foreach ($sub in $subcarpetas) {
    Write-Output "  - Revisando $carpetaLogs\$sub"
}

# Nota interna del tecnico (no modificar)
$notaCodificada = "UmVjb3JkYXRvcmlvIGRlbCB0ZWNuaWNvOiBsYSBjbGF2ZSBkZWwgaW5jaWRlbnRlIGVzIFRIe3Bvd2Vyc2hlbGxfY29kaWZpY2Fkb19ub19jaWZyYWRvXzExfQ=="
$notaTexto = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($notaCodificada))
Write-Output "Nota interna: $notaTexto"

Write-Output "Resumen guardado en $archivoResumen"
Write-Output "Mantenimiento finalizado."
