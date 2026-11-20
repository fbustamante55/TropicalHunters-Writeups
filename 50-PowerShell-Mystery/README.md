# PowerShell Mystery

| | |
|---|---|
| **Categoría** | Scripting / Forensics |
| **Dificultad** | Media |
| **Puntos** | 100 |
| **Reto #** | 50 |

## Descripción

`tarea_programada.ps1` del nodo `AUR-SRV-02` esconde una "nota interna". El script declara 5 variables con fragmentos de Base64 desordenados; la clave está en el orden del `-join`.

## Vulnerabilidad

**Ofuscación por fragmentación y reordenamiento** — el Base64 completo se obtiene concatenando los fragmentos en el orden de `-join`, no en el orden de declaración. Analizar estáticamente el script revela el orden correcto.

## Solución

### 1. Extraer el orden de concatenación

```powershell
# Línea clave del script:
$notaCodificada = -join ($registro, $sello, $marca, $codigo, $etiqueta)
```

Orden: `registro → sello → marca → codigo → etiqueta`

### 2. Reconstruir y decodificar

```python
import base64

# Fragmentos extraídos del .ps1 (sin ejecutar)
registro = "..."
sello    = "..."
marca    = "..."
codigo   = "..."
etiqueta = "..."

s = registro + sello + marca + codigo + etiqueta
print(base64.b64decode(s).decode())
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Fragmentar Base64 en variables desordenadas no añade seguridad; el análisis estático lo reconstruye en segundos.
- Nunca ejecutar scripts de incidentes sin análisis previo en un entorno sandbox.
- El `-join` de PowerShell con orden explícito de variables es la única pista necesaria para resolver el reto.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
