# Time Of Check To Time Of Use

| | |
|---|---|
| **Categoría** | Pwn / Race Condition |
| **Dificultad** | Difícil |
| **Puntos** | 350 |
| **Reto #** | 17 |
| **Conexión** | `chals.tropicalhunters.com:9010` |

## Descripción

El servidor valida un archivo en el momento del *check* y lo vuelve a leer en el momento del *use*, con un `sleep` entre ambas operaciones. Durante esa pausa es posible reemplazar el archivo y hacer que el servidor lea contenido distinto del que validó.

## Vulnerabilidad

**TOCTOU — Time of Check to Time of Use (CWE-367)**

Flujo de `cmd_read`:

1. `lstat(path)` → verifica que es archivo regular
2. `fopen(path, "r")` → lee línea, compara con `"PUBLIC\n"` ✅
3. **`sleep`** ← ventana de carrera
4. `fopen(path, "r")` → lee línea, compara con `"SECRET\n"` → si coincide: `print_flag`

El servidor también expone `cmd_link` que ejecuta `rename(src, dst)` de forma atómica dentro del directorio de sesión — esto permite reemplazar el path durante el sleep.

## Solución

```
Conexión A: write pub "PUBLIC\n"
Conexión A: read pub          → pasa check 1, entra en sleep
Conexión B: write sec "SECRET\n"
Conexión B: link pub sec      → rename(sec, pub)   # durante el sleep
Conexión A: despierta         → fopen("pub") = "SECRET\n" → flag
```

**Script de explotación:** [`exploit.py`](exploit.py) — ejecutar desde Linux con acceso al challenge.

```bash
python3 exploit.py
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- TOCTOU = el estado del recurso puede cambiar entre el check y el use.
- `rename()` es atómico: reemplaza el path sin estado intermedio visible desde otro proceso.
- Cuando un servidor duerme entre verificar y confiar, existe una race window explotable.
- Mitigación: abrir el archivo con `O_NOFOLLOW`, verificar con `fstat` sobre el fd ya abierto, o usar un fd único para check y use.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
